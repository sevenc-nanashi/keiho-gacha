import rawData from "../../extract/data.json";

export type PenalCodeArticle = {
  title: string;
  caption: string;
  text: string;
};

export const penalCodeArticles = rawData as PenalCodeArticle[];
