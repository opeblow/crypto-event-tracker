from enum import Enum
import httpx
from pydantic import BaseModel,Field,HttpUrl
from typing import List,Optional
from datetime import datetime
import os
import re
from dateutil import parser
from dotenv import load_dotenv

load_dotenv()

class SearchNew(str,Enum):
    PAST_DAY="pd"
    PAST_WEEK="pw"
    PAST_MONTH="pm"
    PAST_YEAR="py"
    ALL_TIME=""

class EventCategory(str,Enum):
    CONFERENCE="conference"
    LAUNCH="launch"
    UPGRADE="upgrade"
    AIRDROP="airdrop"
    SUMMIT="summit"
    ANNOUNCEMENT="announcement"
    OTHER="other"

class SearchConfig(BaseModel):
    api_key:str=Field(default_factory=lambda:os.getenv("BRAVE_API_KEY"))
    base_url:str="https://api.search.brave.com/res/v1/web/search"
    results_limit:int=10
    newness:SearchNew=SearchNew.PAST_WEEK

class BraveSearchResult(BaseModel):
    title:str
    url:HttpUrl
    description:str
    age:Optional[str]=None

class CryptoEvent(BaseModel):
    coin_name:str
    event_title:str
    event_date:Optional[datetime]=None
    location:Optional[str]=None
    description:str
    source_url:HttpUrl
    category:EventCategory=EventCategory.OTHER
    has_specific_date:bool=False

    @property
    def is_it_upcoming(self)->bool:
        """Looking to see if event is in the future"""
        if not self.event_date:
            return True
        return self.event_date > datetime.now()
    
class SearchResponse(BaseModel):
    events_with_dates:List[CryptoEvent]=Field(default_factory=list)
    events_without_date:List[CryptoEvent]=Field(default_factory=list)
    total_results:int=0
    query:str

class CryptoSearchTool:
    def __init__(self,config:SearchConfig):
        self.config=config
        self.client=httpx.AsyncClient

        self.crypto_keywords=[
            "bitcoin","btc","ethereum","eth","solana","sol","cardano","ada",
            "ripple","xrp","polkadot","dot","dogecoin","doge","shiba","avalanche",
            "avax","polygon","matic","chainlink","link","litecoin","ltc","uniswap",
            "uni","cosmos","atom","tron","trx","stellar","xlm","monero","xmr",
            "algorand","algo","fantom","ftm","near","aptos","apt","sui","optimism",
            "arbitrum","base","binance","bnb","tether","usdt","usdc"
        ]

        self.category_keywords={
            EventCategory.CONFERENCE:["conference","submit","convention","meetup"],
            EventCategory.LAUNCH:["launch","release","debut","mainnet"],
            EventCategory.UPGRADE:["upgrade","update","hard fork","fork"],
            EventCategory.AIRDROP:["airdrop","token drop","distribution"],
            EventCategory.SUMMIT:["summit","gathering","forum"],
            EventCategory.ANNOUNCEMENT:["announcement","announces","unveils","reveals"]
        }

    async def search(self,query:str,count:Optional[int]=None)->List[BraveSearchResult]:
        """Searches Brave API for crypto events worldwide"""
        headers={
            "Accept":"application/json",
            "X-Subscription-Token":self.config.api_key
        }

        params={
            "q":query,
            "count":count or self.config.results_limit,

        }
        if self.config.newness.value:
            params["newness"]=self.config.newness.value

        response=self.client.get(
            self.config.base_url,
            headers=headers,
            params=params
        )
        response.raise_for_status()
        data=response.json()
        results=[]

        for item in data.get("web",{}).get("results",[]):
            results.append(BraveSearchResult(
                title=item.get("title",""),
                url=item.get("url",""),
                description=item.get("description",""),
                age=item.get("age")

            ))
        return results
    def extract_coin_name(self,text:str)->str:
        """Extracts crypto name from text"""
        text_lower=text.lower()
        for coin in self.crypto_keywords:
            if coin in text_lower:
                return coin.upper()
        return "Unknown"
    

    def extract_category(self,text:str)->str:
        """Extracts Event category name  from text"""
        text_lower=text.lower()
        for category,keywords in self.category_keywords.items():
            for keyword in keywords:
                if keyword in text_lower:
                    return category
        return EventCategory.OTHER
    
    def extract_location(self,text:str)->Optional[str]:
        """Extracts location from text"""
        location_patterns=[
            r"in ([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)",
            r"at ([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)",
            r" ([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)"

        ]
        for pattern in location_patterns:
            match=re.search(pattern,text)
            if match:
                return match.group(1)
        return None
    
    def extract_dates(self,text:str)->List[datetime]:
        """Extracting all possible dates from text"""
        dates=[]
        date_ways=[
            r"\b(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})\b",
            r"\b(\d{4}[/-]\d{1,2}[/-]\d{1,2})\b",
            r"\b(\d{1,2}[A-Z][a-z]+\d{4})\b",
            r"\b([A-Z][a-z]+\d{1,2})\b",
        ]
        for way in date_ways:
            matches=re.findall(way,text)
            for match in matches:
                try:
                    parsed_date=parser.parse(match,fuzzy=True)
                    if len(match.split())<=2  and parsed_date.year==datetime.now().year:
                        if parsed_date< datetime.now():
                            parsed_date=parsed_date.replace(year=datetime.now().year + 1)
                    dates.append(parsed_date)
                except:
                    continue
        return dates
    def parse_events(self,results:List[BraveSearchResult],query:str)->SearchResponse:
        """Parses search results into crypto events(filters only upcoming events)"""
        events_with_dates=[]
        events_without_dates=[]
        for result in results:
            full_text=f"{result.title}{result.description}"
            coin_name=self.extract_coin_name(full_text)
            category=self.extract_category(full_text)
            location=self.extract_location(full_text)
            dates=self.extract_dates(full_text)

            event_date=dates[0] if dates else None
            has_date=event_date is not None
            event=CryptoEvent(
                coin_name=coin_name,
                event_title=result.title,
                event_date=event_date,
                location=location,
                description=result.description,
                source_url=result.url,
                category=category,
                has_specific_date=has_date
            )
            if event.is_it_upcoming:
                if event.has_specific_date:
                    events_with_dates.append(event)
                else:
                    events_without_dates.append(event)
        return SearchResponse(
            events_with_dates=events_with_dates,
            events_without_date=events_without_dates,
            total_results=len(results),
            query=query
        )
    async def close(self):
        self.client.close()
                