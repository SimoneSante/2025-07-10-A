from dataclasses import dataclass

@dataclass
class Category:
    category_id:int
    category_name:str

    def __hash__(self):
        return hash(self.product_id)

    def __eq__(self,other):
        return self.product_id == other.product_id

    def __str__(self):
        return f"{self.product_name}"