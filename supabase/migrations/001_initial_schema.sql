-- ════════════════════════════════════════════════════════════════════
-- CareerFit AI — Supabase Database Schema
-- Run this in: Supabase Dashboard → SQL Editor → New Query → Run
-- ════════════════════════════════════════════════════════════════════

-- ── 1. Profiles table ───────────────────────────────────────────────
-- Stores user profile info synced from Supabase Auth (Google OAuth).
-- The id column references auth.users so every row maps 1:1 to a
-- logged-in user.

CREATE TABLE IF NOT EXISTS public.profiles (
    id          UUID PRIMARY KEY REFERENCES auth.users(id) ON DELETE CASCADE,
    email       TEXT NOT NULL,
    full_name   TEXT,
    avatar_url  TEXT,
    created_at  TIMESTAMPTZ DEFAULT now() NOT NULL,
    updated_at  TIMESTAMPTZ DEFAULT now() NOT NULL
);

-- Enable RLS (Row Level Security) so users can only see their own data.
ALTER TABLE public.profiles ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Users can view their own profile"
    ON public.profiles FOR SELECT
    USING (auth.uid() = id);

CREATE POLICY "Users can update their own profile"
    ON public.profiles FOR UPDATE
    USING (auth.uid() = id);

-- ── 2. Auto-create profile on signup ────────────────────────────────
-- This trigger fires when a new user signs up via Google OAuth and
-- copies basic info from the auth.users metadata into our profiles table.

CREATE OR REPLACE FUNCTION public.handle_new_user()
RETURNS TRIGGER
LANGUAGE plpgsql
SECURITY DEFINER SET search_path = ''
AS $$
BEGIN
    INSERT INTO public.profiles (id, email, full_name, avatar_url)
    VALUES (
        NEW.id,
        NEW.email,
        COALESCE(NEW.raw_user_meta_data ->> 'full_name', NEW.raw_user_meta_data ->> 'name', ''),
        COALESCE(NEW.raw_user_meta_data ->> 'avatar_url', NEW.raw_user_meta_data ->> 'picture', '')
    );
    RETURN NEW;
END;
$$;

-- Drop existing trigger if re-running this migration
DROP TRIGGER IF EXISTS on_auth_user_created ON auth.users;

CREATE TRIGGER on_auth_user_created
    AFTER INSERT ON auth.users
    FOR EACH ROW
    EXECUTE FUNCTION public.handle_new_user();


-- ── 3. Interview sessions table ─────────────────────────────────────
-- Each row represents one interview practice session.
-- Tied to a user via user_id (FK to profiles.id).

CREATE TABLE IF NOT EXISTS public.interview_sessions (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id         UUID NOT NULL REFERENCES public.profiles(id) ON DELETE CASCADE,
    title           TEXT,                                        -- e.g. "Frontend React Developer"
    job_description TEXT NOT NULL,                                -- raw JD text
    persona         JSONB,                                       -- AI-generated interviewer persona
    status          TEXT NOT NULL DEFAULT 'created'               -- created | in_progress | completed
                        CHECK (status IN ('created', 'in_progress', 'completed')),
    created_at      TIMESTAMPTZ DEFAULT now() NOT NULL,
    updated_at      TIMESTAMPTZ DEFAULT now() NOT NULL
);

ALTER TABLE public.interview_sessions ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Users can manage their own sessions"
    ON public.interview_sessions FOR ALL
    USING (auth.uid() = user_id);


-- ── 4. Conversation messages table ──────────────────────────────────
-- Stores each turn of the interview (user question / agent response).

CREATE TABLE IF NOT EXISTS public.conversation_messages (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    session_id      UUID NOT NULL REFERENCES public.interview_sessions(id) ON DELETE CASCADE,
    role            TEXT NOT NULL CHECK (role IN ('user', 'assistant')),
    content         TEXT NOT NULL,
    turn_number     INTEGER NOT NULL,
    created_at      TIMESTAMPTZ DEFAULT now() NOT NULL
);

ALTER TABLE public.conversation_messages ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Users can manage messages in their own sessions"
    ON public.conversation_messages FOR ALL
    USING (
        EXISTS (
            SELECT 1 FROM public.interview_sessions s
            WHERE s.id = session_id AND s.user_id = auth.uid()
        )
    );


-- ── 5. Feedback reports table ───────────────────────────────────────
-- Stores the Coach Agent's structured JSON feedback after an interview.

CREATE TABLE IF NOT EXISTS public.feedback_reports (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    session_id      UUID NOT NULL UNIQUE REFERENCES public.interview_sessions(id) ON DELETE CASCADE,
    report          JSONB NOT NULL,                              -- structured feedback JSON
    created_at      TIMESTAMPTZ DEFAULT now() NOT NULL
);

ALTER TABLE public.feedback_reports ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Users can view feedback for their own sessions"
    ON public.feedback_reports FOR SELECT
    USING (
        EXISTS (
            SELECT 1 FROM public.interview_sessions s
            WHERE s.id = session_id AND s.user_id = auth.uid()
        )
    );


-- ── 6. Indexes for performance ──────────────────────────────────────
CREATE INDEX IF NOT EXISTS idx_interview_sessions_user_id
    ON public.interview_sessions(user_id);

CREATE INDEX IF NOT EXISTS idx_conversation_messages_session_id
    ON public.conversation_messages(session_id);

CREATE INDEX IF NOT EXISTS idx_feedback_reports_session_id
    ON public.feedback_reports(session_id);


-- ── 7. Updated_at auto-refresh trigger ──────────────────────────────
CREATE OR REPLACE FUNCTION public.update_updated_at_column()
RETURNS TRIGGER
LANGUAGE plpgsql
AS $$
BEGIN
    NEW.updated_at = now();
    RETURN NEW;
END;
$$;

CREATE TRIGGER set_profiles_updated_at
    BEFORE UPDATE ON public.profiles
    FOR EACH ROW
    EXECUTE FUNCTION public.update_updated_at_column();

CREATE TRIGGER set_sessions_updated_at
    BEFORE UPDATE ON public.interview_sessions
    FOR EACH ROW
    EXECUTE FUNCTION public.update_updated_at_column();
