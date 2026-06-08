from typing import Any, Optional
from chief_executive_agent import ChiefExecutiveAgent
from meeting_secretary import MeetingTranscriber, MeetingManager, MinutesGenerator
from business_analyst import BusinessAnalyzer, RiskDetector, SummaryEngine
from document_intelligence import PDFGenerator, ReportBuilder, ProposalBuilder
from crm_agent import ClientManager, OpportunityManager
from scheduling_agent import CalendarManager, ReminderManager, NotificationDispatcher
from memory_agent import VectorStore, KnowledgeBase, EmbeddingService
from legal_agent import ContractManager, LegalReviewer
from financial_agent import BudgetManager, CashFlowManager, FinancialReportGenerator
from notification_agent import WhatsAppNotifier, EmailNotifier, PushNotifier
from sales_agent import LeadManager, PipelineManager


class AgentsBridge:
    def __init__(self, company_id: str, openai_api_key: Optional[str] = None):
        self.company_id = company_id
        self.cea = ChiefExecutiveAgent(company_id, openai_api_key)
        self.meeting_secretary = MeetingManager()
        self.meeting_transcriber = MeetingTranscriber(openai_api_key)
        self.minutes_generator = MinutesGenerator(openai_api_key)
        self.business_analyzer = BusinessAnalyzer()
        self.risk_detector = RiskDetector()
        self.summary_engine = SummaryEngine()
        self.pdf_generator = PDFGenerator()
        self.report_builder = ReportBuilder()
        self.proposal_builder = ProposalBuilder()
        self.crm = ClientManager()
        self.opportunities = OpportunityManager()
        self.calendar = CalendarManager()
        self.reminders = ReminderManager()
        self.notifications = NotificationDispatcher()
        self.knowledge_base = KnowledgeBase()
        self.vector_store = VectorStore()
        self.embeddings = EmbeddingService(openai_api_key)
        self.legal = ContractManager()
        self.legal_reviewer = LegalReviewer()
        self.budgets = BudgetManager()
        self.cashflow = CashFlowManager()
        self.financial_reports = FinancialReportGenerator()
        self.whatsapp = WhatsAppNotifier()
        self.email = EmailNotifier()
        self.push = PushNotifier()
        self.sales_leads = LeadManager()
        self.sales_pipeline = PipelineManager()

    async def process_request(self, request: str, context: dict[str, Any]) -> dict[str, Any]:
        return await self.cea.process_request(request, context)
