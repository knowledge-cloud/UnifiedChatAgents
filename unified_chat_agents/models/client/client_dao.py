from models import BaseDAO
from models.client.client_model import Client


class ClientDAO(BaseDAO[Client]):
    def get_client(self,id: str) -> Client:
        return self.get(Client, id)

    def save_client(self, id: str, organization_id: str, name: str, base_url: str) -> Client:
        client = Client(id=id, organization_id=organization_id,
                        name=name, base_url=base_url)
        return self.save(client)


clientDAOInstance = ClientDAO()
