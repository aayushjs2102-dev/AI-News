-- ==========================================================
-- AI News
-- PostgreSQL Database Schema
-- ==========================================================

-- ----------------------------------------------------------
-- USERS
-- ----------------------------------------------------------

CREATE TABLE users (
    id SERIAL PRIMARY KEY,

    username VARCHAR(50) NOT NULL UNIQUE,

    email VARCHAR(255) NOT NULL UNIQUE,

    password_hash TEXT NOT NULL,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ----------------------------------------------------------
-- ARTICLES
-- ----------------------------------------------------------

CREATE TABLE articles (
    id SERIAL PRIMARY KEY,

    source VARCHAR(100) NOT NULL,

    title TEXT NOT NULL,

    summary TEXT NOT NULL,

    url TEXT NOT NULL UNIQUE,

    published_at TIMESTAMP NOT NULL,

    collected_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    category VARCHAR(100) NOT NULL,

    cluster_id VARCHAR(100)
);

-- ----------------------------------------------------------
-- USER INTERACTIONS
-- ----------------------------------------------------------

CREATE TABLE user_interactions (
    id SERIAL PRIMARY KEY,

    user_id INTEGER NOT NULL,

    article_id INTEGER NOT NULL,

    interaction_type VARCHAR(20) NOT NULL,

    interaction_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_user
        FOREIGN KEY(user_id)
        REFERENCES users(id)
        ON DELETE CASCADE,

    CONSTRAINT fk_article
        FOREIGN KEY(article_id)
        REFERENCES articles(id)
        ON DELETE CASCADE,

    CONSTRAINT chk_interaction
        CHECK (
            interaction_type IN
            (
                'view',
                'like',
                'bookmark'
            )
        )
);

-- ----------------------------------------------------------
-- USER CLUSTER PREFERENCES
-- ----------------------------------------------------------

CREATE TABLE user_cluster_preferences (
    id SERIAL PRIMARY KEY,

    user_id INTEGER NOT NULL,

    cluster_id VARCHAR(100) NOT NULL,

    preference_score DOUBLE PRECISION DEFAULT 0,

    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_cluster_user
        FOREIGN KEY(user_id)
        REFERENCES users(id)
        ON DELETE CASCADE,

    CONSTRAINT unique_user_cluster
        UNIQUE(user_id, cluster_id)
);

-- ==========================================================
-- INDEXES
-- ==========================================================

CREATE INDEX idx_articles_category
ON articles(category);

CREATE INDEX idx_articles_cluster
ON articles(cluster_id);

CREATE INDEX idx_articles_published
ON articles(published_at);

CREATE INDEX idx_interactions_user
ON user_interactions(user_id);

CREATE INDEX idx_interactions_article
ON user_interactions(article_id);

CREATE INDEX idx_preferences_user
ON user_cluster_preferences(user_id);

CREATE INDEX idx_preferences_cluster
ON user_cluster_preferences(cluster_id);