import requests
from typing import Dict, Any
import logging

logger = logging.getLogger(__name__)

class PricingDataCollector:
    """
    Collects real-time market data, customer behavior data, and competitive insights.
    
    Attributes:
        api_keys: Dictionary containing API keys for different data sources.
        data_sources: List of URLs or endpoints from which to collect data.
    """
    
    def __init__(self, config):
        self.api_keys = config['api_keys']
        self.data_sources = config['data_sources']
        
    def fetch_market_data(self) -> Dict[str, Any]:
        """
        Fetches market conditions such as demand, supply, and economic indicators.
        
        Returns:
            Dictionary containing market data.
        """
        try:
            response = requests.get(f"{self.data_sources['market']}/current")
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Failed to fetch market data: {str(e)}")
            return None
            
    def fetch_customer_behavior(self) -> Dict[str, Any]:
        """
        Retrieves customer behavior patterns and preferences.
        
        Returns:
            Dictionary containing customer behavior data.
        """
        try:
            response = requests.get(
                f"{self.data_sources['customer']}/behavior", 
                params={'api_key': self.api_keys['customer']}
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Failed to fetch customer behavior: {str(e)}")
            return None
            
    def fetch_competitive_data(self) -> Dict[str, Any]:
        """
        Collects competitive pricing data from the market.
        
        Returns:
            Dictionary containing competitor data.
        """
        try:
            response = requests.get(
                f"{self.data_sources['competitor']}/prices", 
                params={'api_key': self.api_keys['competitor']}
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Failed to fetch competitor data: {str(e)}")
            return None
            
    def collect(self) -> Dict[str, Any]:
        """
        Aggregates and returns all collected pricing-related data.
        
        Returns:
            Dictionary containing aggregated data.
        """
        data = {
            'market': self.fetch_market_data(),
            'customer': self.fetch_customer_behavior(),
            'competitor': self.fetch_competitive_data()
        }
        
        # Filter out None values
        filtered_data = {k: v for k, v in data.items() if v is not None}
        return filtered_data