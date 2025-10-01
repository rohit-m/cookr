import { createClient } from '@supabase/supabase-js'

// Supabase client initialization
// Make sure to set VITE_SUPABASE_URL and VITE_SUPABASE_ANON_KEY in supabase.env
const supabaseUrl = import.meta.env.VITE_SUPABASE_URL
const supabaseAnonKey = import.meta.env.VITE_SUPABASE_ANON_KEY

export const supabase = createClient(supabaseUrl, supabaseAnonKey)

