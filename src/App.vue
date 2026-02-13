<script setup lang="ts">
import { computed, ref, watch } from "vue";
import { keihoArticles, kenpoArticles, type Article } from "./data/articles";
import { randBetween } from "./math";

type GachaResult = {
  roll: number;
  type: "keiho" | "kenpo";
  article: Article;
  id: string;
};

type GachaLog = {
  id: number;
  count: number;
  lawLabel: string;
  results: GachaResult[];
};

const results = ref<GachaResult[]>([]);
const logs = ref<GachaLog[]>([]);
const isKenpoMode = ref(false);
let nextLogId = 1;
const targetLawLabel = computed(() => (isKenpoMode.value ? "憲法" : "刑法"));
const targetArticles = computed(() =>
  isKenpoMode.value ? kenpoArticles : keihoArticles,
);

const twitterLink = computed(() => {
  const baseUrl = "https://twitter.com/intent/tweet";
  const target = isKenpoMode.value ? "憲法" : "刑法";
  let text = `#${target}のランダムな条文を廃止する党 は、${target}の__remaining__を廃止することを宣言いたします。`;
  const maxLength = 129;
  for (const result of results.value) {
    if (text.length + result.article.title.length + 2 <= maxLength) {
      text = text.replace(
        "__remaining__",
        `${result.article.title}、__remaining__`,
      );
    } else {
      text = text.replace("__remaining__", "等");
      break;
    }
  }
  if (text.includes("__remaining__")) {
    text = text.replace("__remaining__", "等");
  }
  const url = encodeURIComponent(location.href);
  return `${baseUrl}?text=${encodeURIComponent(text)}&url=${url}`;
});

const draw = (count: number): void => {
  const nextResults: GachaResult[] = [];

  for (let i = 0; i < count; i += 1) {
    const randomIndex = Math.floor(Math.random() * targetArticles.value.length);
    const article = targetArticles.value[randomIndex];

    if (article === undefined) {
      throw new Error("法令条文データの取得に失敗しました");
    }

    nextResults.push({
      roll: i + 1,
      type: isKenpoMode.value ? "kenpo" : "keiho",
      article,
      id: crypto.randomUUID(),
    });
  }

  results.value = nextResults;
  // vueはunshiftをリアクティブに検知しないため、新しい配列を作成して代入する
  logs.value = [
    {
      id: nextLogId,
      count,
      lawLabel: targetLawLabel.value,
      results: nextResults,
    },
    ...logs.value,
  ];
  nextLogId += 1;
};

const keihoMultiGachaTexts = ["激アツ！", "出血大サービス！", "法改正の嵐！"];
const kenpoMultiGachaTexts = ["激アツ！", "出血大サービス！", "国民投票の嵐！"];
const kenpoWithout96GachaTexts = [
  "激アツ！",
  "出血大サービス！",
  "憲法改正の嵐！",
];
const multiGachaText = ref("激アツ！");
watch(
  [isKenpoMode, logs],
  () => {
    const texts = isKenpoMode.value
      ? logs.value.some((log) =>
          log.results.some(
            (result) =>
              result.type === "kenpo" && result.article.title === "第九十六条",
          ),
        )
        ? kenpoWithout96GachaTexts
        : kenpoMultiGachaTexts
      : keihoMultiGachaTexts;
    multiGachaText.value = texts[randBetween(0, texts.length - 1)];
  },
  { immediate: true },
);
</script>

<template>
  <main class="container">
    <header class="hero">
      <h1>{{ targetLawLabel }}のランダムな条文を廃止する党</h1>
      <p>ボタンを押して{{ targetLawLabel }}を廃止しよう！</p>
      <p>
        作った人：<a
          href="https://sevenc7c.com"
          target="_blank"
          rel="noopener noreferrer"
          >Nanashi.</a
        >（とCodex CLI）
      </p>
      <p>
        ソースコード：<a
          href="https://github.com/sevenc-nanashi/keiho-gacha"
          target="_blank"
          rel="noopener noreferrer"
          >sevenc-nanashi/keiho-gacha</a
        >
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

    <section class="law-selector" aria-label="対象法令の切り替え">
      <label class="switch">
        <span class="switch-label">対象法令</span>
        <input
          v-model="isKenpoMode"
          class="switch-input"
          type="checkbox"
          role="switch"
          :aria-checked="isKenpoMode"
          :aria-label="`対象法令を${targetLawLabel}に切り替え`"
        />
        <span class="switch-slider" aria-hidden="true"></span>
        <span class="switch-value">{{ targetLawLabel }}</span>
      </label>
    </section>

    <section class="actions" aria-label="ガチャ操作">
      <button type="button" class="button" @click="draw(1)">1連</button>
      <button type="button" class="button primary" @click="draw(10)">
        {{ multiGachaText }} 10連
      </button>
    </section>

    <section class="results" aria-live="polite">
      <p v-if="results.length === 0" class="hint">まだ引いていません</p>
      <template v-else>
        <div class="share-results">
          <a
            :href="twitterLink"
            target="_blank"
            rel="noopener noreferrer"
            class="button twitter-button"
          >
            結果をTwitterでシェアする
          </a>
        </div>
        <ol>
          <li v-for="result in results" :key="result.id">
            <article class="card latest-result">
              <p class="roll">{{ result.roll }}連目</p>
              <h2>
                {{ result.article.title }}
                <span v-if="result.article.caption" class="caption"
                  >- {{ result.article.caption }}
                </span>
              </h2>
              <p class="result-content">{{ result.article.text }}</p>
            </article>
          </li>
        </ol>
      </template>
    </section>

    <section
      v-if="logs.length > 0"
      class="history"
      aria-label="過去のガチャログ"
    >
      <h2>過去のガチャログ</h2>
      <ol class="history-list">
        <li v-for="log in logs" :key="log.id" class="history-item">
          <p class="history-meta">
            第{{ log.id }}回（{{ log.lawLabel }} / {{ log.count }}連）
          </p>
          <ul class="history-results">
            <li v-for="result in log.results" :key="result.id">
              {{ result.roll }}連目: {{ result.article.title }}
              {{ result.article.caption ? "- " + result.article.caption : "" }}
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

.share-results {
  margin-bottom: 1rem;
}
.button.twitter-button {
  background-color: #1da1f2;
  color: #ffffff;
}
</style>
