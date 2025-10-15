import React from "react";

export default function Home() {
  return (
    <main style={{fontFamily: "system-ui, sans-serif", padding: 24, maxWidth: 840, margin: "0 auto"}}>
      <h1>SSVproff</h1>
      <p>Стартовая витрина проекта. Быстрые ссылки:</p>
      <ul>
        <li><a href="https://github.com/Serg2206/SSVproff">Репозиторий</a></li>
        <li><a href="/docs/">Документация (GitHub Pages)</a></li>
        <li><a href="http://localhost:8001/health">API Health (локально)</a></li>
      </ul>
      <p style={{opacity:0.8}}>Сайт собирается статически и публикуется через GitHub Pages.</p>
    </main>
  );
}
