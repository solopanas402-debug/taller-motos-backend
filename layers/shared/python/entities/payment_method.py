"""
Payment Method Entity
Define the available payment methods with translations
"""

class PaymentMethod:
    """Payment method enumeration with translations"""
    
    PAYMENT_METHODS = {
        'cash': {
            'value': 'cash',
            'label': 'Efectivo',
            'description': 'Pago en efectivo'
        },
        'transfer': {
            'value': 'transfer',
            'label': 'Transferencia',
            'description': 'Transferencia bancaria'
        },
        'debit_card': {
            'value': 'debit_card',
            'label': 'Tarjeta de débito',
            'description': 'Pago con tarjeta de débito'
        },
        'credit_card': {
            'value': 'credit_card',
            'label': 'Tarjeta de crédito',
            'description': 'Pago con tarjeta de crédito'
        }
    }
    
    @classmethod
    def get_all(cls) -> list:
        """Get all payment methods as a list"""
        return list(cls.PAYMENT_METHODS.values())
    
    @classmethod
    def get_by_value(cls, value: str) -> dict | None:
        """Get payment method by value"""
        return cls.PAYMENT_METHODS.get(value)
    
    @classmethod
    def is_valid(cls, value: str) -> bool:
        """Check if a value is a valid payment method"""
        return value in cls.PAYMENT_METHODS
    
    @classmethod
    def get_values(cls) -> list:
        """Get list of valid payment method values"""
        return list(cls.PAYMENT_METHODS.keys())
    
    @classmethod
    def get_labels(cls) -> dict:
        """Get mapping of values to labels"""
        return {k: v['label'] for k, v in cls.PAYMENT_METHODS.items()}
