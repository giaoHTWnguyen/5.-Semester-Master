from pathlib import Path

BASE = Path(__file__).parent
DATA = BASE / 'data'
KATALOGE = BASE / 'fragenkataloge'
ERGEBNISSE = BASE / 'results'
FIGURES = BASE.parent / 'thesis' / 'figures'

for p in (DATA, KATALOGE, ERGEBNISSE, FIGURES):
    p.mkdir(parents=True, exist_ok=True)

MODEL_OPENAI = 'gpt-5.6-luna'
MODEL_GOOGLE = 'gemini-3.6-flash'

MODELS = [('openai', MODEL_OPENAI), ('google', MODEL_GOOGLE)]

# neutraler System-Prompt, englisch

SYSTEM_PROMPT_EXP0 = "You are a data analyst answering questions about exploratory data analysis. Answer factually and precisely."
SYSTEM_PROMPT_EXP1 = "You are a data analyst answering questions about exploratory data analysis. Answer the user's questions about the provided dataset factually and precisely."

METRIC_COLUMNS = [
    'Age', 'MonthlyIncome', 'DailyRate', 'MonthlyRate', 'HourlyRate',
    'DistanceFromHome', 'TotalWorkingYears', 'YearsAtCompany',
    'YearsInCurrentRole', 'YearsSinceLastPromotion',
    'YearsWithCurrManager', 'NumCompaniesWorked', 'PercentSalaryHike',
    'TrainingTimesLastYear',
]


# --- Reproduzierbarkeit ----

SEED = 42 # used for the OverTime permutation in E2

# --- Model access ----

TEMPERATURE       = 1          # fixed by GPT, set identically for Gemini
MAX_OUTPUT_TOKENS = 8000
CACHE_TTL_SECONDS = 7200       # Google explicit context cache
ITERATIONS_EXP0   = 3
ITERATIONS_DATA   = 5          # experiments 1 and 2

### Referenz Computation ####

NULL_VARIANCE_COLUMNS = ["EmployeeCount", "StandardHours", "Over18"]
BINARY_ENCODING       = {"Yes": 1, "No": 0}
IQR_FACTOR            = 1.5    # outlier threshold
N_BINS                = 3      # quantile binning: low, medium, high
SPECIAL_BINS          = {"YearsSinceLastPromotion": [-1, 1, 5, None]}
EXCLUDED_FROM_RULES   = ["YearsInCurrentRole", "YearsWithCurrManager"]

# --- Association rules (Hammesfahr & Spott, 2021) --------------------
MIN_SUPPORT       = 0.05
MIN_IMPROVEMENT   = 0.05       # minimal improvement threshold
# minimum confidence = median confidence of the initial rule set

# --- Manipulation for experiment 2 -----------------------------------
MANIPULATED_COLUMN  = "OverTime"
TARGET_YES_LEAVERS  = 33       # leavers assigned to OverTime = Yes
                               # -> 7.9 % vs 19.4 %, reversing the original
                               # relation while preserving both marginals

# --- Scoring ---------------------------------------------------------
TOLERANCE_FULL      = 0.02     # <= 2 % relative deviation -> 2 points
TOLERANCE_PARTIAL   = 0.05     # <= 5 % relative deviation -> 1 point
SCALE_MAX_DATA      = 2        # categories A and B
SCALE_MAX_EXP0      = 3