export type UserRole = 'customer' | 'professional' | 'admin';

export interface User {
  id: number;
  email: string;
  phone?: string;
  role: UserRole;
  is_active: boolean;
  created_at?: string;
  profile?: CustomerProfile | ProfessionalProfile;
}

export interface CustomerProfile {
  id: number;
  user_id: number;
  full_name: string;
  profile_photo?: string;
  city?: string;
  locality?: string;
  pin_code?: string;
  email?: string;
  phone?: string;
}

export interface Skill {
  id: number;
  category_id: number;
  category_name?: string;
  is_primary: boolean;
}

export interface PortfolioItem {
  id: number;
  title?: string;
  description?: string;
  image_url: string;
}

export interface ProfessionalProfile {
  id: number;
  user_id: number;
  full_name: string;
  profile_photo?: string;
  introduction?: string;
  service_description?: string;
  years_of_experience: number;
  employment_type?: string;
  city: string;
  locality?: string;
  pin_code?: string;
  travel_distance_km?: number;
  pricing_type: string;
  price_amount?: number;
  currency: string;
  availability: string;
  is_verified: boolean;
  verification_status?: string;
  profile_visits?: number;
  average_rating?: number | null;
  review_count?: number;
  skills: Skill[];
  portfolio_items: PortfolioItem[];
  phone?: string;
  whatsapp?: string;
  show_phone_publicly?: boolean;
  whatsapp_consent?: boolean;
  created_at?: string;
}

export interface ServiceCategory {
  id: number;
  name: string;
  slug: string;
  description?: string;
  icon?: string;
  sort_order?: number;
}

export interface ProjectInquiry {
  id: number;
  customer_id: number;
  professional_id: number;
  work_description: string;
  location?: string;
  expected_start_date?: string;
  approximate_budget?: number;
  currency: string;
  status: string;
  customer_name?: string;
  professional_name?: string;
  created_at?: string;
  updated_at?: string;
}

export interface PaginatedResponse<T> {
  items: T[];
  total: number;
  page: number;
  per_page: number;
  pages: number;
}
