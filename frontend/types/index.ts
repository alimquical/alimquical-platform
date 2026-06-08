export interface User {
  id: string;
  email: string;
  name: string;
  role: "admin" | "manager" | "user";
  company_id: string;
  avatar?: string;
}

export interface Company {
  id: string;
  name: string;
  plan: "starter" | "business" | "corporate";
  active: boolean;
  created_at: string;
}

export interface Meeting {
  id: string;
  title: string;
  date: string;
  duration: number;
  status: "scheduled" | "completed" | "cancelled";
  transcript?: string;
  summary?: string;
  participants: string[];
  company_id: string;
}

export interface Client {
  id: string;
  name: string;
  email: string;
  phone: string;
  company: string;
  status: "active" | "inactive" | "lead";
  last_contact: string;
}

export interface Document {
  id: string;
  title: string;
  type: "pdf" | "doc" | "xls" | "image";
  size: number;
  uploaded_by: string;
  created_at: string;
  tags: string[];
}

export interface Task {
  id: string;
  title: string;
  description?: string;
  status: "todo" | "in_progress" | "done";
  priority: "low" | "medium" | "high";
  assignee?: string;
  due_date?: string;
  meeting_id?: string;
}

export interface SubscriptionPlan {
  id: string;
  name: string;
  price: number;
  interval: "monthly" | "yearly";
  meetings_limit: number;
  users_limit: number;
  features: string[];
}

export interface AgentStatus {
  name: string;
  status: "active" | "idle" | "error";
  last_active: string;
  tasks_completed: number;
}
