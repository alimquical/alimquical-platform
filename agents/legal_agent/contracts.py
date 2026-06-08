from typing import Any, Optional


class ContractManager:
    def __init__(self):
        self.contracts = {}

    def create_contract(self, title: str, parties: list[str], clauses: list[dict]) -> dict[str, Any]:
        contract_id = f"ctr_{len(self.contracts) + 1}"
        contract = {
            "id": contract_id,
            "title": title,
            "parties": parties,
            "clauses": clauses,
            "status": "draft",
            "created_at": "2026-06-15",
        }
        self.contracts[contract_id] = contract
        return contract

    def get_contract(self, contract_id: str) -> Optional[dict]:
        return self.contracts.get(contract_id)
