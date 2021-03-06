/* global window */

export const MAX_EXPERIENCE = 45;
export const MIN_EXPERIENCE = 0;

export const HISTOGRAM_BINS = 12;

// TODO: This is duplicated from server-side code; consolidate it.
export const EDU_HIGH_SCHOOL = 'HS';
export const EDU_ASSOCIATES = 'AA';
export const EDU_BACHELORS = 'BA';
export const EDU_MASTERS = 'MA';
export const EDU_PHD = 'PHD';

export const EDU_LABELS = {
  [EDU_HIGH_SCHOOL]: 'High School',
  [EDU_ASSOCIATES]: 'Associates',
  [EDU_BACHELORS]: 'Bachelors Degree',
  [EDU_MASTERS]: 'Masters Degree',
  [EDU_PHD]: 'Ph.D',
};

export const BUSINESS_SIZE_LABELS = {
  s: 'small business',
  o: 'other than small',
};

export const SITE_LABELS = {
  customer: 'customer',
  contractor: 'contractor',
  both: 'both',
};

const SCHEDULES = [{
  SIN: 899,
  schedule: 'Environmental',
  name: 'Legacy Environmental',
}, {
  SIN: 87405,
  schedule: 'Logistics',
  name: 'Legacy Logistics',
}, {
  SIN: 874,
  schedule: 'MOBIS',
  name: 'Legacy MOBIS',
}, {
  SIN: 871,
  schedule: 'PES',
  name: 'Legacy PES',
}, {
  SIN: 73802,
  schedule: 'Language Services',
  name: 'Legacy Language',
}, {
  SIN: 541,
  schedule: 'AIMS',
  name: 'Legacy AIMS',
}, {
  SIN: 520,
  schedule: 'FABS',
  name: 'Legacy FABS',
}, {
  SIN: 132,
  schedule: 'IT Schedule 70',
  name: 'IT 70',
}];

export const SCHEDULE_LABELS = {};

SCHEDULES.forEach(({ SIN, schedule, name }) => {
  SCHEDULE_LABELS[schedule] = `${SIN} - ${name}`;
});

SCHEDULE_LABELS.Consolidated = 'Consolidated';

export const CONTRACT_YEAR_CURRENT = 'current';
export const CONTRACT_YEAR_1 = '1';
export const CONTRACT_YEAR_2 = '2';

export const CONTRACT_YEAR_LABELS = {
  [CONTRACT_YEAR_CURRENT]: 'Current year',
  [CONTRACT_YEAR_1]: 'One year out',
  [CONTRACT_YEAR_2]: 'Two years out',
};

export const DEFAULT_CONTRACT_YEAR = 'current';

export const EMPTY_RATES_DATA = {
  minimum: 0,
  maximum: 0.001,
  average: 0,
  first_standard_deviation: 0,
  count: 0,
  results: [],
  wage_histogram: [
    { count: 0, min: 0, max: 0 },
  ],
};

export const DEFAULT_SORT = { key: 'current_price', descending: false };

export const SORT_KEYS = [
  'labor_category',
  'education_level',
  'min_years_experience',
  'current_price',
  'idv_piid',
  'vendor_name',
  'schedule',
];

export const QUERY_TYPE_MATCH_ALL = 'match_all';

export const QUERY_TYPE_MATCH_PHRASE = 'match_phrase';

export const QUERY_TYPE_MATCH_EXACT = 'match_exact';

export const DEFAULT_QUERY_TYPE = QUERY_TYPE_MATCH_ALL;

export const QUERY_TYPE_LABELS = {
  [QUERY_TYPE_MATCH_ALL]: 'Contains words',
  [QUERY_TYPE_MATCH_PHRASE]: 'Contains phrase',
  [QUERY_TYPE_MATCH_EXACT]: 'Exact match',
};

export const API_HOST = window.API_HOST;

export const API_RATES_CSV = `${API_HOST}rates/csv/`;
