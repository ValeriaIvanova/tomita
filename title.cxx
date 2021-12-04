#encoding "utf8"

Type -> 'книга' | 'журнал' | 'статья';
Title -> Word<h-reg1, l-quoted, ~r-quoted> AnyWord<~r-quoted>+ Word<~l-quoted, r-quoted>;


S -> Type interp(Titles.Type) Title interp(Titles.Title::not_norm);