const buttons = [...document.querySelectorAll('[data-filter]')];
const cards = [...document.querySelectorAll('.project-card')];
const groups = [...document.querySelectorAll('[data-project-group]')];
const search = document.querySelector('#project-search');
const empty = document.querySelector('#empty');
let category = 'all';

function filterCards() {
  const query = search.value.trim().toLocaleLowerCase();
  let visible = 0;
  for (const card of cards) {
    card.hidden = (category !== 'all' && card.dataset.category !== category)
      || !card.dataset.search.includes(query);
    if (!card.hidden) visible++;
  }
  for (const group of groups) {
    group.hidden = ![...group.querySelectorAll('.project-card')].some((card) => !card.hidden);
  }
  empty.hidden = visible !== 0;
}

for (const button of buttons) button.addEventListener('click', () => {
  category = button.dataset.filter;
  for (const option of buttons) option.setAttribute('aria-pressed', String(option === button));
  filterCards();
});
search.addEventListener('input', filterCards);
