from repositories.customer_repository import CustomerRepository


class CustomerUseCase:
    def __init__(self, customer_repository: CustomerRepository):
        self.customer_repository = customer_repository

    def is_customer_exists(self, id_customer):
        print("Begin is_customer_exists")
        result = True
        try:
            customer = self.customer_repository.get(id_customer)
            if not customer:
                result = False
        except Exception as e:
            print(f"Ha ocurrido un problema en customer_use_case: {e}")
            result = False

        return result
