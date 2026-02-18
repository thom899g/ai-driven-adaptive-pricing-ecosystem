from typing import Dict, Any
import logging
from .models import PricingModel

logger = logging.getLogger(__name__)

class PricingEngine:
    """
    Core engine responsible for dynamic pricing calculations.
    
    Attributes:
        model: Instance of the pricing prediction model.
        config: Configuration parameters for pricing strategy.
    """
    
    def __init__(self, model: PricingModel, config: Dict[str, Any]):
        self.model = model
        self.config = config
        
    def calculate_optimal_price(self, data: Dict[str, Any]) -> float:
        """
        Uses machine learning models to compute the optimal price.
        
        Args:
            data: Dictionary containing market, customer, and competitor data.
            
        Returns:
            The calculated optimal price as a float.
        """
        try:
            # Feature engineering
            features = self._ engineer_features(data)
            
            # Predict price
            predicted_price = self.model.predict(features)
            
            # Apply business rules
            adjusted_price = self._adjust_for_business_rules(predicted_price)
            
            return adjusted_price
        except Exception as e:
            logger.error(f"Failed to calculate optimal price: {str(e)}")
            return None
            
    def _engineer_features(self, data: Dict[str, Any]) -> Dict[str, float]:
        """
        Creates features from raw data for the pricing model.
        
        Args:
            data: Dictionary containing market, customer, and competitor data.
            
        Returns:
            Dictionary of engineered features.
        """
        features = {}
        
        # Market features
        if data.get('market'):
            features['market_demand'] = data['market'].get('demand', 0)
            features['economic_indicator'] = data['market'].get('economic_indicator', 0)
            
        # Customer features
        if data.get('customer'):
            features['customer_preference'] = data['customer'].get('preference_score', 0)
            features['seasonal_pattern'] = data['customer'].get('seasonal_patterns', {})
            
        # Competitor features
        if data.get('competitor'):
            features['competitor_price_avg'] = data['competitor'].get('avg_price', 0)
            features['competitor_count'] = len(data['competitor'].get('prices', []))
            
        return features
        
    def _adjust_for_business_rules(self, predicted_price: float) -> float:
        """
        Adjusts the predicted price based on business rules and constraints.
        
        Args:
            predicted_price: The price predicted by the model.
            
        Returns:
            The adjusted price considering business rules.
        """
        min_price = self.config.get('min_price', 0)
        max_price = self.config.get('max_price', float('inf'))
        
        # Apply clamp
        clamped_price = max(min(predicted_price, max_price), min_price)
        
        # Apply discounts or surcharges based on business rules
        if self.config.get('seasonal_discount'):
            discount = 0.1  # Example discount
            clamped_price *= (1 - discount)
            
        return round(clamped_price, 2)  # Assuming prices are in currency with 2 decimals
        
    def update_model(self, new_data: Dict[str, Any]) -> None:
        """
        Updates the underlying machine learning model with new data.
        
        Args:
            new_data: New training data to incorporate into the model.
        """
        try:
            self.model.train(new_data)
        except Exception as e:
            logger.error(f"Failed to update pricing model: {str(e)}")