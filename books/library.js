// רשימת הספרים בספרייה.
// כדי להוסיף ספר חדש:
//   1. יוצרים תיקייה books/<id>/ ובה קובץ book.js (אפשר להעתיק את books/yud-bereshit/book.js כתבנית)
//   2. מוסיפים כאן רשומה עם אותו id
// ספר עם status: "soon" יופיע בספרייה כ"בקרוב" בלי אפשרות קריאה.
window.LIBRARY = [
  {
    id: "yud-bereshit",
    series: "יוּד הַקְּטַנָּה",
    chapter: 1,
    status: "available",
    src: "books/yud-bereshit/book.js?v=2"
  }
];
