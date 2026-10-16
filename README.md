# ספרייה קטנה

אתר ספרי ילדים מאוירים בעברית (RTL), מותאם לנייד. האתר סטטי לגמרי, בלי שלב בנייה: HTML, CSS ו־JavaScript פשוטים.

## מבנה

```
index.html              מעטפת האתר
css/style.css           עיצוב
js/config.js            הגדרות: שם האתר, קישור תרומה (זמני)
js/app.js               ניתוב, ספרייה, כריכה, קורא עם החלקה, עמוד "על המיזם"
books/library.js        רשימת הספרים
books/<id>/book.js      תוכן של ספר: טקסט, איורי SVG, שאלות, פרקים הבאים
```

כתובות (hash routing, עובד ב־GitHub Pages בלי הגדרות):
`#/` ספרייה · `#/book/<id>` כריכה · `#/book/<id>/<n>` עמוד · `#/about` על המיזם

## הוספת ספר חדש

1. מעתיקים את `books/yud-bereshit/book.js` לתיקייה חדשה, למשל `books/yud-sarah/book.js`.
2. משנים `id`, כותרות, `pages` (לכל עמוד: `text`, `bg`, `art` עם SVG), `questions`, `nextChapters`.
3. מוסיפים רשומה ל־`books/library.js` עם אותו `id` ו־`src`.

## קישור התרומה

ב־`js/config.js` מחליפים את `donateUrl` בקישור האמיתי.

## פרסום ב־GitHub Pages

ב־Settings ← Pages בוחרים Source: **GitHub Actions**. כל דחיפה ל־`main` מפרסמת את האתר דרך `.github/workflows/pages.yml`.

## הרצה מקומית

```
python3 -m http.server 8000
```
ואז לפתוח http://localhost:8000
