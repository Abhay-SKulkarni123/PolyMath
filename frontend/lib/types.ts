export interface User {
  id: number;
  email: string;
  first_name: string;
  last_name: string;
  role: string;
}

export interface KnowledgeField {
  id: number;
  name: string;
  slug: string;
  icon: string;
}

export interface Product {
  id: number;
  vendor_name: string;
  knowledge_fields: KnowledgeField[];
  name: string;
  description: string;
  price: string;
  stock: number;
  type: string;
  file: string | null;
  cover_image: string | null;
  is_active: boolean;
  created_at: string;
}

export interface CartItem {
  id: number;
  product: Product;
  quantity: number;
  item_total: number;
}

export interface Cart {
  id: number;
  items: CartItem[];
  total_price: number;
}

export interface OrderItem {
  id: number;
  product_name: string;
  product_type: string;
  quantity: number;
  price: string;
  item_total: number;
  download_url: string | null;
}

export interface Order {
  id: number;
  status: string;
  shipping_address: string;
  total_price: string;
  items: OrderItem[];
  created_at: string;
}

export interface Movie {
  order: number;
  id: number;
  tmdb_id: number;
  title: string;
  overview: string;
  poster_path: string;
  backdrop_path: string;
  poster_url: string;
  backdrop_url: string;
  release_date: string;
  vote_average: number;
  vote_count: number;
  popularity: number;
  type: string;
  watch_url: string;
  is_featured: boolean;
}

export interface Collection {
  id: number;
  name: string;
  slug: string;
  description: string;
  icon: string;
  banner_path: string;
  poster_path: string;
  banner_url: string;
  poster_url: string;
  category: string;
  order: number;
  movie_count: number;
  top_movies: Movie[];
  movies?: Movie[];
}
