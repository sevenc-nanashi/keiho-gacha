<script setup lang="ts">
import { ref } from "vue";
import { penalCodeArticles, type PenalCodeArticle } from "./data/articles";

type GachaResult = {
  roll: number;
  article: PenalCodeArticle;
  id: string;
};

type GachaLog = {
  id: number;
  count: number;
  results: GachaResult[];
};

const results = ref<GachaResult[]>([]);
const logs = ref<GachaLog[]>([]);
let nextLogId = 1;

const draw = (count: number): void => {
  const nextResults: GachaResult[] = [];

  for (let i = 0; i < count; i += 1) {
    const randomIndex = Math.floor(Math.random() * penalCodeArticles.length);
    const article = penalCodeArticles[randomIndex];

    if (article === undefined) {
      throw new Error("刑法条文データの取得に失敗しました");
    }

    nextResults.push({
      roll: i + 1,
      article,
      id: crypto.randomUUID(),
    });
  }

  results.value = nextResults;
  logs.value.unshift({
    id: nextLogId,
    count,
    results: nextResults,
  });
  nextLogId += 1;
};

const multiGachaTexts = ["激アツ！", "出血大サービス！", "法改正の嵐！"];
const multiGachaText = multiGachaTexts[
  Math.floor(Math.random() * multiGachaTexts.length)
] as string;
</script>

<template>
  <main class="container">
    <header class="hero">
      <h1>刑法のランダムな条文を廃止する党</h1>
      <p>ボタンを押して刑法を廃止しよう！</p>
      <p>
        作った人：<a
          href="https://sevenc7c.com"
          target="_blank"
          rel="noopener noreferrer"
          >Nanashi.</a
        >（とCodex CLI）
      </p>
      <p>
        元ネタ：<a
          href="https://twitter.com/windymelt/status/2021908111066632317"
          target="_blank"
          rel="noopener noreferrer"
          >Windymelt</a
        >
      </p>
      <p class="note">
        ※これはジョークアプリです。実際の法改正には関係ありません。
      </p>
    </header>

    <section class="actions" aria-label="ガチャ操作">
      <button type="button" class="button" @click="draw(1)">1連</button>
      <button type="button" class="button primary" @click="draw(10)">
        {{ multiGachaText }} 10連
      </button>
    </section>

    <section class="results" aria-live="polite">
      <p v-if="results.length === 0" class="hint">まだ引いていません</p>
      <ol v-else>
        <li v-for="result in results" :key="result.id">
          <article class="card latest-result">
            <p class="roll">{{ result.roll }}連目</p>
            <h2>
              {{ result.article.title }}
              <span v-if="result.article.caption" class="caption"
                >- {{ result.article.caption }}
              </span>
            </h2>
            <p>{{ result.article.text }}</p>
          </article>
        </li>
      </ol>
    </section>

    <section
      v-if="logs.length > 0"
      class="history"
      aria-label="過去のガチャログ"
    >
      <h2>過去のガチャログ</h2>
      <ol class="history-list">
        <li v-for="log in logs" :key="log.id" class="history-item">
          <p class="history-meta">第{{ log.id }}回（{{ log.count }}連）</p>
          <ul class="history-results">
            <li v-for="result in log.results" :key="result.id">
              {{ result.roll }}連目: {{ result.article.title }} {{ result.article.caption ? "- " + result.article.caption : "" }}
            </li>
          </ul>
        </li>
      </ol>
    </section>
  </main>
</template>

<style scoped>
.latest-result {
  transition: border-color 0.3s ease-in-out;

  @starting-style {
    border-color: #ff9800;
  }
}
</style>
