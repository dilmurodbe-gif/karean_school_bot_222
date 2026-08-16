import sqlite3
from datetime import datetime
from config import DATABASE_PATH


# ============================================================
# DATABASE CONNECTION
# ============================================================

def get_connection():
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row

    # Foreign keylarni yoqish
    conn.execute("PRAGMA foreign_keys = ON")

    return conn


# ============================================================
# DATABASE INITIALIZATION
# ============================================================

def init_db():
    conn = get_connection()
    cur = conn.cursor()

    try:

        # ====================================================
        # FOYDALANUVCHILAR
        # ====================================================

        cur.execute("""
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                first_name TEXT,
                username TEXT,
                joined_at TEXT NOT NULL
            )
        """)

        # ====================================================
        # PREMIUM FOYDALANUVCHILAR
        # ====================================================

        cur.execute("""
            CREATE TABLE IF NOT EXISTS premium_users (
                user_id INTEGER PRIMARY KEY,
                is_active INTEGER NOT NULL DEFAULT 1,
                activated_at TEXT NOT NULL,
                FOREIGN KEY (user_id) REFERENCES users(user_id)
            )
        """)

        # ====================================================
        # TO'LOVLAR
        # ====================================================

        cur.execute("""
            CREATE TABLE IF NOT EXISTS payments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                payment_method TEXT NOT NULL,
                amount TEXT NOT NULL,
                receipt_file_id TEXT NOT NULL,
                receipt_type TEXT NOT NULL,
                status TEXT NOT NULL DEFAULT 'pending',
                created_at TEXT NOT NULL,
                reviewed_at TEXT,
                reviewed_by INTEGER,
                FOREIGN KEY (user_id) REFERENCES users(user_id)
            )
        """)

        # ====================================================
        # KURSLAR
        # ====================================================

        cur.execute("""
            CREATE TABLE IF NOT EXISTS courses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                code TEXT UNIQUE NOT NULL,
                description TEXT
            )
        """)

        # ====================================================
        # KURS BO'LIMLARI
        # ====================================================

        cur.execute("""
            CREATE TABLE IF NOT EXISTS course_sections (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                course_id INTEGER NOT NULL,
                title TEXT NOT NULL,
                position INTEGER NOT NULL DEFAULT 1,
                FOREIGN KEY (course_id) REFERENCES courses(id)
            )
        """)

        # ====================================================
        # VIDEO DARSLAR
        # ====================================================

        cur.execute("""
            CREATE TABLE IF NOT EXISTS video_lessons (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                section_id INTEGER NOT NULL,
                title TEXT NOT NULL,
                video_file_id TEXT,
                description TEXT,
                position INTEGER NOT NULL DEFAULT 1,
                FOREIGN KEY (section_id) REFERENCES course_sections(id)
            )
        """)

        # ====================================================
        # BUGUNGI GRAMMATIKA
        # ====================================================

        cur.execute("""
            CREATE TABLE IF NOT EXISTS daily_grammar (
                id INTEGER PRIMARY KEY,
                photo_file_id TEXT,
                text TEXT,
                created_at TEXT NOT NULL,
                expires_at TEXT NOT NULL,
                remind_sent INTEGER NOT NULL DEFAULT 0,
                views INTEGER DEFAULT 0
            )
        """)

        # Eski database uchun ustunlarni tekshirish
        cur.execute("PRAGMA table_info(daily_grammar)")
        columns = [row["name"] for row in cur.fetchall()]

        if "remind_sent" not in columns:
            try:
                cur.execute("""
                    ALTER TABLE daily_grammar
                    ADD COLUMN remind_sent INTEGER NOT NULL DEFAULT 0
                """)
            except sqlite3.OperationalError:
                pass

        # ====================================================
        # BUGUNGI GRAMMATIKA ARXIVI
        # ====================================================

        cur.execute("""
            CREATE TABLE IF NOT EXISTS daily_grammar_archive (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                photo_file_id TEXT,
                text TEXT,
                created_at TEXT,
                expires_at TEXT,
                views INTEGER DEFAULT 0
            )
        """)

        # ====================================================
        # PODCASTLAR
        # ====================================================

        cur.execute("""
            CREATE TABLE IF NOT EXISTS podcasts (
                id INTEGER PRIMARY KEY,
                title TEXT NOT NULL,
                video TEXT NOT NULL,
                pdf TEXT
            )
        """)

        # ====================================================
        # AI TEACHER
        # ====================================================

        cur.execute("""
            CREATE TABLE IF NOT EXISTS ai_teacher_questions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                username TEXT,
                first_name TEXT,
                question TEXT NOT NULL,
                admin_message_id INTEGER,
                answer TEXT,
                status TEXT NOT NULL DEFAULT 'pending',
                created_at TEXT NOT NULL,
                answered_at TEXT
            )
        """)

        # ====================================================
        # KITOB BO'LIMLARI
        # ====================================================

        cur.execute("""
            CREATE TABLE IF NOT EXISTS book_sections (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL UNIQUE
            )
        """)

        # ====================================================
        # KITOBLAR
        # ====================================================

        cur.execute("""
            CREATE TABLE IF NOT EXISTS book_items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                section_id INTEGER NOT NULL,
                title TEXT NOT NULL,
                post_text TEXT,
                book_link TEXT NOT NULL,
                channel_link TEXT,
                updated_at TEXT NOT NULL,

                UNIQUE(section_id, title),

                FOREIGN KEY (section_id)
                    REFERENCES book_sections(id)
                    ON DELETE CASCADE
            )
        """)

        # ====================================================
        # KITOBLAR
        # ====================================================

        cur.execute("""
                    CREATE TABLE IF NOT EXISTS book_sections
                    (
                        id
                        INTEGER
                        PRIMARY
                        KEY
                        AUTOINCREMENT,
                        title
                        TEXT
                        NOT
                        NULL
                        UNIQUE
                    )
                    """)

        cur.execute("""
                    CREATE TABLE IF NOT EXISTS book_items
                    (
                        id
                        INTEGER
                        PRIMARY
                        KEY
                        AUTOINCREMENT,
                        section_id
                        INTEGER
                        NOT
                        NULL,
                        title
                        TEXT
                        NOT
                        NULL,
                        post_text
                        TEXT,
                        book_link
                        TEXT
                        NOT
                        NULL,
                        channel_link
                        TEXT,
                        updated_at
                        TEXT,
                        FOREIGN
                        KEY
                    (
                        section_id
                    )
                        REFERENCES book_sections
                    (
                        id
                    )
                        ON DELETE CASCADE,
                        UNIQUE
                    (
                        section_id,
                        title
                    )
                        )
                    """)

        # ====================================================
        # 3 TA ASOSIY KURS
        # ====================================================

        courses = [
            (
                "🌱 Boshlang'ich",
                "beginner",
                "Koreys tilini 0 dan o'rganish"
            ),
            (
                "🥉 TOPIK 1",
                "topik1",
                "TOPIK 1 uchun tayyorlov kursi"
            ),
            (
                "🥇 TOPIK 2",
                "topik2",
                "TOPIK 2 uchun tayyorlov kursi"
            )
        ]

        for title, code, description in courses:
            cur.execute("""
                INSERT OR IGNORE INTO courses (
                    title,
                    code,
                    description
                )
                VALUES (?, ?, ?)
            """, (
                title,
                code,
                description
            ))

        # ====================================================
        # SAQLASH
        # ====================================================

        conn.commit()

    except Exception:
        conn.rollback()
        raise

    finally:
        conn.close()


# ============================================================
# FOYDALANUVCHILAR
# ============================================================

def add_user(
    user_id: int,
    first_name: str,
    username: str | None
):
    conn = get_connection()

    try:
        cur = conn.cursor()

        cur.execute("""
            INSERT INTO users (
                user_id,
                first_name,
                username,
                joined_at
            )
            VALUES (?, ?, ?, ?)

            ON CONFLICT(user_id) DO UPDATE SET
                first_name=excluded.first_name,
                username=excluded.username
        """, (
            user_id,
            first_name or "",
            username or "",
            datetime.now().isoformat()
        ))

        conn.commit()

    finally:
        conn.close()


def get_user_by_id(user_id: int):
    conn = get_connection()

    try:
        cur = conn.cursor()

        cur.execute("""
            SELECT *
            FROM users
            WHERE user_id=?
        """, (user_id,))

        return cur.fetchone()

    finally:
        conn.close()


def get_all_users():
    conn = get_connection()

    try:
        cur = conn.cursor()

        cur.execute("""
            SELECT *
            FROM users
            ORDER BY joined_at DESC
        """)

        return cur.fetchall()

    finally:
        conn.close()


def get_users_count():
    conn = get_connection()

    try:
        cur = conn.cursor()

        cur.execute("""
            SELECT COUNT(*)
            FROM users
        """)

        return cur.fetchone()[0]

    finally:
        conn.close()


# ============================================================
# PREMIUM
# ============================================================

def is_premium(user_id: int) -> bool:
    conn = get_connection()

    try:
        cur = conn.cursor()

        cur.execute("""
            SELECT is_active
            FROM premium_users
            WHERE user_id=?
        """, (user_id,))

        row = cur.fetchone()

        return bool(row and row["is_active"] == 1)

    finally:
        conn.close()


def activate_premium(user_id: int):
    conn = get_connection()

    try:
        cur = conn.cursor()

        cur.execute("""
            INSERT INTO premium_users (
                user_id,
                is_active,
                activated_at
            )
            VALUES (?, 1, ?)

            ON CONFLICT(user_id) DO UPDATE SET
                is_active=1,
                activated_at=excluded.activated_at
        """, (
            user_id,
            datetime.now().isoformat()
        ))

        conn.commit()

    finally:
        conn.close()


def deactivate_premium(user_id: int):
    conn = get_connection()

    try:
        cur = conn.cursor()

        cur.execute("""
            UPDATE premium_users
            SET is_active=0
            WHERE user_id=?
        """, (user_id,))

        conn.commit()

    finally:
        conn.close()


def get_all_premium_users():
    conn = get_connection()

    try:
        cur = conn.cursor()

        cur.execute("""
            SELECT
                users.user_id,
                users.first_name,
                users.username,
                premium_users.activated_at
            FROM premium_users
            LEFT JOIN users
                ON users.user_id = premium_users.user_id
            WHERE premium_users.is_active=1
            ORDER BY premium_users.activated_at DESC
        """)

        return cur.fetchall()

    finally:
        conn.close()


def get_premium_count():
    conn = get_connection()

    try:
        cur = conn.cursor()

        cur.execute("""
            SELECT COUNT(*)
            FROM premium_users
            WHERE is_active=1
        """)

        return cur.fetchone()[0]

    finally:
        conn.close()


# ============================================================
# TO'LOVLAR
# ============================================================

def create_payment(
    user_id: int,
    payment_method: str,
    amount: str,
    receipt_file_id: str,
    receipt_type: str
) -> int:

    conn = get_connection()

    try:
        cur = conn.cursor()

        cur.execute("""
            INSERT INTO payments (
                user_id,
                payment_method,
                amount,
                receipt_file_id,
                receipt_type,
                status,
                created_at
            )
            VALUES (?, ?, ?, ?, ?, 'pending', ?)
        """, (
            user_id,
            payment_method,
            amount,
            receipt_file_id,
            receipt_type,
            datetime.now().isoformat()
        ))

        payment_id = cur.lastrowid

        conn.commit()

        return payment_id

    finally:
        conn.close()


def get_payment(payment_id: int):
    conn = get_connection()

    try:
        cur = conn.cursor()

        cur.execute("""
            SELECT *
            FROM payments
            WHERE id=?
        """, (payment_id,))

        return cur.fetchone()

    finally:
        conn.close()


def get_pending_payment_by_user(user_id: int):
    conn = get_connection()

    try:
        cur = conn.cursor()

        cur.execute("""
            SELECT *
            FROM payments
            WHERE user_id=?
              AND status='pending'
            ORDER BY id DESC
            LIMIT 1
        """, (user_id,))

        return cur.fetchone()

    finally:
        conn.close()


def approve_payment(payment_id: int, admin_id: int):
    conn = get_connection()

    try:
        cur = conn.cursor()

        cur.execute("""
            UPDATE payments
            SET
                status='approved',
                reviewed_at=?,
                reviewed_by=?
            WHERE id=?
        """, (
            datetime.now().isoformat(),
            admin_id,
            payment_id
        ))

        conn.commit()

    finally:
        conn.close()


def reject_payment(payment_id: int, admin_id: int):
    conn = get_connection()

    try:
        cur = conn.cursor()

        cur.execute("""
            UPDATE payments
            SET
                status='rejected',
                reviewed_at=?,
                reviewed_by=?
            WHERE id=?
        """, (
            datetime.now().isoformat(),
            admin_id,
            payment_id
        ))

        conn.commit()

    finally:
        conn.close()


def get_pending_payments_count():
    conn = get_connection()

    try:
        cur = conn.cursor()

        cur.execute("""
            SELECT COUNT(*)
            FROM payments
            WHERE status='pending'
        """)

        return cur.fetchone()[0]

    finally:
        conn.close()


def get_payment_history_by_user(user_id: int):
    conn = get_connection()

    try:
        cur = conn.cursor()

        cur.execute("""
            SELECT *
            FROM payments
            WHERE user_id=?
            ORDER BY id DESC
        """, (user_id,))

        return cur.fetchall()

    finally:
        conn.close()


# ============================================================
# KURSLAR
# ============================================================

def get_courses():
    conn = get_connection()

    try:
        cur = conn.cursor()

        cur.execute("""
            SELECT *
            FROM courses
            ORDER BY id
        """)

        return cur.fetchall()

    finally:
        conn.close()


def get_course_by_code(code: str):
    conn = get_connection()

    try:
        cur = conn.cursor()

        cur.execute("""
            SELECT *
            FROM courses
            WHERE code=?
        """, (code,))

        return cur.fetchone()

    finally:
        conn.close()


# ============================================================
# KURS BO'LIMLARI
# ============================================================

def get_sections(course_id: int):
    conn = get_connection()

    try:
        cur = conn.cursor()

        cur.execute("""
            SELECT *
            FROM course_sections
            WHERE course_id=?
            ORDER BY position, id
        """, (course_id,))

        return cur.fetchall()

    finally:
        conn.close()


def get_section(section_id: int):
    conn = get_connection()

    try:
        cur = conn.cursor()

        cur.execute("""
            SELECT *
            FROM course_sections
            WHERE id=?
        """, (section_id,))

        return cur.fetchone()

    finally:
        conn.close()


def delete_section(section_id: int):
    conn = get_connection()

    try:
        cur = conn.cursor()

        cur.execute("""
            DELETE FROM video_lessons
            WHERE section_id=?
        """, (section_id,))

        cur.execute("""
            DELETE FROM course_sections
            WHERE id=?
        """, (section_id,))

        conn.commit()

    finally:
        conn.close()


# ============================================================
# VIDEO DARSLAR
# ============================================================

def get_lessons(section_id: int):
    conn = get_connection()

    try:
        cur = conn.cursor()

        cur.execute("""
            SELECT *
            FROM video_lessons
            WHERE section_id=?
            ORDER BY position, id
        """, (section_id,))

        return cur.fetchall()

    finally:
        conn.close()


def get_lesson(lesson_id: int):
    conn = get_connection()

    try:
        cur = conn.cursor()

        cur.execute("""
            SELECT *
            FROM video_lessons
            WHERE id=?
        """, (lesson_id,))

        return cur.fetchone()

    finally:
        conn.close()


def delete_lesson(lesson_id: int):
    conn = get_connection()

    try:
        cur = conn.cursor()

        cur.execute("""
            DELETE FROM video_lessons
            WHERE id=?
        """, (lesson_id,))

        conn.commit()

    finally:
        conn.close()


def update_lesson_title(
    lesson_id: int,
    new_title: str
):
    conn = get_connection()

    try:
        cur = conn.cursor()

        cur.execute("""
            UPDATE video_lessons
            SET title=?
            WHERE id=?
        """, (
            new_title,
            lesson_id
        ))

        conn.commit()

    finally:
        conn.close()


def update_lesson_description(
    lesson_id: int,
    new_description: str
):
    conn = get_connection()

    try:
        cur = conn.cursor()

        cur.execute("""
            UPDATE video_lessons
            SET description=?
            WHERE id=?
        """, (
            new_description,
            lesson_id
        ))

        conn.commit()

    finally:
        conn.close()


def update_lesson_video(
    lesson_id: int,
    video_file_id: str
):
    conn = get_connection()

    try:
        cur = conn.cursor()

        cur.execute("""
            UPDATE video_lessons
            SET video_file_id=?
            WHERE id=?
        """, (
            video_file_id,
            lesson_id
        ))

        conn.commit()

    finally:
        conn.close()


# ============================================================
# BUGUNGI GRAMMATIKA
# ============================================================

def create_daily_grammar(
    photo_file_id: str | None,
    text: str,
    expires_at: str
):
    conn = get_connection()

    try:
        cur = conn.cursor()

        cur.execute("""
            SELECT
                photo_file_id,
                text,
                created_at,
                expires_at,
                views
            FROM daily_grammar
            WHERE id=1
        """)

        old = cur.fetchone()

        if old:
            cur.execute("""
                INSERT INTO daily_grammar_archive (
                    photo_file_id,
                    text,
                    created_at,
                    expires_at,
                    views
                )
                VALUES (?, ?, ?, ?, ?)
            """, (
                old["photo_file_id"],
                old["text"],
                old["created_at"],
                old["expires_at"],
                old["views"] or 0
            ))

            cur.execute("""
                DELETE FROM daily_grammar
                WHERE id=1
            """)

        cur.execute("""
            INSERT INTO daily_grammar (
                id,
                photo_file_id,
                text,
                created_at,
                expires_at,
                remind_sent,
                views
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            1,
            photo_file_id,
            text,
            datetime.now().isoformat(),
            expires_at,
            0,
            0
        ))

        conn.commit()

    finally:
        conn.close()


def get_daily_grammar():
    conn = get_connection()

    try:
        cur = conn.cursor()

        cur.execute("""
            SELECT
                photo_file_id,
                text,
                expires_at
            FROM daily_grammar
            WHERE id=1
        """)

        return cur.fetchone()

    finally:
        conn.close()


def get_daily_grammar_for_reminder():
    conn = get_connection()

    try:
        cur = conn.cursor()

        cur.execute("""
            SELECT
                photo_file_id,
                text,
                expires_at,
                remind_sent
            FROM daily_grammar
            WHERE id=1
        """)

        return cur.fetchone()

    finally:
        conn.close()


def mark_daily_grammar_reminded():
    conn = get_connection()

    try:
        cur = conn.cursor()

        cur.execute("""
            UPDATE daily_grammar
            SET remind_sent=1
            WHERE id=1
        """)

        conn.commit()

    finally:
        conn.close()


def expire_daily_grammar():
    conn = get_connection()

    try:
        cur = conn.cursor()

        cur.execute("""
            SELECT
                photo_file_id,
                text,
                created_at,
                expires_at,
                views
            FROM daily_grammar
            WHERE id=1
        """)

        old = cur.fetchone()

        if old:
            cur.execute("""
                INSERT INTO daily_grammar_archive (
                    photo_file_id,
                    text,
                    created_at,
                    expires_at,
                    views
                )
                VALUES (?, ?, ?, ?, ?)
            """, (
                old["photo_file_id"],
                old["text"],
                old["created_at"],
                old["expires_at"],
                old["views"] or 0
            ))

            cur.execute("""
                DELETE FROM daily_grammar
                WHERE id=1
            """)

        conn.commit()

    finally:
        conn.close()


def delete_daily_grammar():
    conn = get_connection()

    try:
        cur = conn.cursor()

        cur.execute("""
            DELETE FROM daily_grammar
            WHERE id=1
        """)

        conn.commit()

    finally:
        conn.close()


def increase_daily_grammar_views():
    conn = get_connection()

    try:
        cur = conn.cursor()

        cur.execute("""
            UPDATE daily_grammar
            SET views = COALESCE(views, 0) + 1
            WHERE id=1
        """)

        conn.commit()

    finally:
        conn.close()


# ============================================================
# PODCASTLAR
# ============================================================

def get_all_podcasts():
    conn = get_connection()

    try:
        cur = conn.cursor()

        cur.execute("""
            SELECT
                id,
                title,
                video,
                pdf
            FROM podcasts
            ORDER BY id
        """)

        rows = cur.fetchall()

        podcasts = {}

        for row in rows:
            podcasts[row["id"]] = {
                "title": row["title"],
                "video": row["video"],
                "pdf": row["pdf"]
            }

        return podcasts

    finally:
        conn.close()


def get_podcast(podcast_id: int):
    conn = get_connection()

    try:
        cur = conn.cursor()

        cur.execute("""
            SELECT
                id,
                title,
                video,
                pdf
            FROM podcasts
            WHERE id=?
        """, (podcast_id,))

        row = cur.fetchone()

        if not row:
            return None

        return {
            "id": row["id"],
            "title": row["title"],
            "video": row["video"],
            "pdf": row["pdf"]
        }

    finally:
        conn.close()


def add_podcast(
    podcast_id: int,
    title: str,
    video: str,
    pdf: str | None = None
):
    conn = get_connection()

    try:
        cur = conn.cursor()

        cur.execute("""
            INSERT INTO podcasts (
                id,
                title,
                video,
                pdf
            )
            VALUES (?, ?, ?, ?)
        """, (
            podcast_id,
            title,
            video,
            pdf
        ))

        conn.commit()

    finally:
        conn.close()


def delete_podcast(podcast_id: int):
    conn = get_connection()

    try:
        cur = conn.cursor()

        cur.execute("""
            DELETE FROM podcasts
            WHERE id=?
        """, (podcast_id,))

        conn.commit()

    finally:
        conn.close()


# ============================================================
# AI TEACHER
# ============================================================

def init_ai_teacher_table():
    conn = get_connection()

    try:
        cur = conn.cursor()

        cur.execute("""
            CREATE TABLE IF NOT EXISTS ai_teacher_questions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                username TEXT,
                first_name TEXT,
                question TEXT NOT NULL,
                admin_message_id INTEGER,
                answer TEXT,
                status TEXT NOT NULL DEFAULT 'pending',
                created_at TEXT NOT NULL,
                answered_at TEXT
            )
        """)

        conn.commit()

    finally:
        conn.close()


def create_ai_teacher_question(
    user_id: int,
    username: str,
    first_name: str,
    question: str,
    admin_message_id: int
):
    conn = get_connection()

    try:
        cur = conn.cursor()

        cur.execute("""
            INSERT INTO ai_teacher_questions (
                user_id,
                username,
                first_name,
                question,
                admin_message_id,
                status,
                created_at
            )
            VALUES (?, ?, ?, ?, ?, 'pending', ?)
        """, (
            user_id,
            username,
            first_name,
            question,
            admin_message_id,
            datetime.now().isoformat()
        ))

        question_id = cur.lastrowid

        conn.commit()

        return question_id

    finally:
        conn.close()


def get_ai_teacher_question(question_id: int):
    conn = get_connection()

    try:
        cur = conn.cursor()

        cur.execute("""
            SELECT *
            FROM ai_teacher_questions
            WHERE id=?
        """, (question_id,))

        return cur.fetchone()

    finally:
        conn.close()


def get_ai_teacher_question_by_admin_message(
    admin_message_id: int
):
    conn = get_connection()

    try:
        cur = conn.cursor()

        cur.execute("""
            SELECT *
            FROM ai_teacher_questions
            WHERE admin_message_id=?
            LIMIT 1
        """, (admin_message_id,))

        return cur.fetchone()

    finally:
        conn.close()


def answer_ai_teacher_question(
    question_id: int,
    answer: str
):
    conn = get_connection()

    try:
        cur = conn.cursor()

        cur.execute("""
            UPDATE ai_teacher_questions
            SET
                answer=?,
                status='answered',
                answered_at=?
            WHERE id=?
        """, (
            answer,
            datetime.now().isoformat(),
            question_id
        ))

        conn.commit()

    finally:
        conn.close()


def get_ai_teacher_daily_count(user_id: int):
    conn = get_connection()

    try:
        cur = conn.cursor()

        cur.execute("""
            SELECT COUNT(*)
            FROM ai_teacher_questions
            WHERE user_id=?
              AND date(created_at) = date('now', 'localtime')
        """, (user_id,))

        return cur.fetchone()[0]

    finally:
        conn.close()


# ============================================================
# KITOB BO'LIMLARI
# ============================================================

def get_book_sections():
    conn = get_connection()

    try:
        cur = conn.cursor()

        cur.execute("""
            SELECT
                id,
                title
            FROM book_sections
            ORDER BY title
        """)

        return cur.fetchall()

    finally:
        conn.close()


def get_book_section(section_id: int):
    conn = get_connection()

    try:
        cur = conn.cursor()

        cur.execute("""
            SELECT
                id,
                title
            FROM book_sections
            WHERE id=?
        """, (section_id,))

        return cur.fetchone()

    finally:
        conn.close()


def create_book_section(title: str):
    conn = get_connection()

    try:
        cur = conn.cursor()

        cur.execute("""
            INSERT INTO book_sections (
                title
            )
            VALUES (?)
        """, (title,))

        section_id = cur.lastrowid

        conn.commit()

        return section_id

    finally:
        conn.close()


def delete_book_section(section_id: int):
    conn = get_connection()

    try:
        cur = conn.cursor()

        # ON DELETE CASCADE sababli
        # ichidagi kitoblar ham o'chadi
        cur.execute("""
            DELETE FROM book_sections
            WHERE id=?
        """, (section_id,))

        conn.commit()

    finally:
        conn.close()


# ============================================================
# KITOBLAR
# ============================================================

def get_books_by_section(section_id: int):
    conn = get_connection()

    try:
        cur = conn.cursor()

        cur.execute("""
            SELECT
                id,
                section_id,
                title,
                post_text,
                book_link,
                channel_link,
                updated_at
            FROM book_items
            WHERE section_id=?
            ORDER BY title
        """, (section_id,))

        return cur.fetchall()

    finally:
        conn.close()


def get_book(book_id: int):
    conn = get_connection()

    try:
        cur = conn.cursor()

        cur.execute("""
            SELECT
                id,
                section_id,
                title,
                post_text,
                book_link,
                channel_link,
                updated_at
            FROM book_items
            WHERE id=?
        """, (book_id,))

        return cur.fetchone()

    finally:
        conn.close()


def create_book(
    section_id: int,
    title: str,
    post_text: str,
    book_link: str,
    channel_link: str
):
    conn = get_connection()

    try:
        cur = conn.cursor()

        cur.execute("""
            INSERT INTO book_items (
                section_id,
                title,
                post_text,
                book_link,
                channel_link,
                updated_at
            )
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            section_id,
            title,
            post_text,
            book_link,
            channel_link,
            datetime.now().isoformat()
        ))

        book_id = cur.lastrowid

        conn.commit()

        return book_id

    finally:
        conn.close()


def update_book(
    book_id: int,
    title: str,
    post_text: str,
    book_link: str,
    channel_link: str
):
    conn = get_connection()

    try:
        cur = conn.cursor()

        cur.execute("""
            UPDATE book_items
            SET
                title=?,
                post_text=?,
                book_link=?,
                channel_link=?,
                updated_at=?
            WHERE id=?
        """, (
            title,
            post_text,
            book_link,
            channel_link,
            datetime.now().isoformat(),
            book_id
        ))

        conn.commit()

    finally:
        conn.close()


def delete_book(book_id: int):
    conn = get_connection()

    try:
        cur = conn.cursor()

        cur.execute("""
            DELETE FROM book_items
            WHERE id=?
        """, (book_id,))

        conn.commit()

    finally:
        conn.close()


def get_books_count():
    conn = get_connection()

    try:
        cur = conn.cursor()

        cur.execute("""
            SELECT COUNT(*)
            FROM book_items
        """)

        return cur.fetchone()[0]

    finally:
        conn.close()


def get_book_sections_count():
    conn = get_connection()

    try:
        cur = conn.cursor()

        cur.execute("""
            SELECT COUNT(*)
            FROM book_sections
        """)

        return cur.fetchone()[0]

    finally:
        conn.close()
