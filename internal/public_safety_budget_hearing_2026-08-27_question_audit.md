# August 27-labelled public safety hearing: question and response audit

Source: `public_safety_budget_hearing_2026-08-27.json`. All timestamps refer to the supplied excerpt.

## Findings

I coded **99 substantive spoken questions**, including **68 follow-up questions**. I also identified **12 document/data requests**, of which **10 were follow-ups. Including those requests gives **111 information requests and 78 follow-ups**.

Public Safety supplied **40 direct answers to spoken questions**, plus one direct response confirming that requested documents had been sent: **41 requests directly answered in all**. Direct means responsive to the actual question, not independently verified as true. There were also **29 partial question replies involving Public Safety**, including mixed replies where another office contributed.

I identified **8 distinct Public Safety commitments to check, investigate or report back**. Finance/Business Administrator made **6 additional commitments**, and one grant-budget commitment has uncertain office attribution. Repeating a promise within the same exchange counts once.

There were **9 clear Public Safety uncertainty episodes**, plus **11 additional episodes of tentative or hedged recall: **20 using the broader definition**. One additional vehicle-audit exchange is ambiguous as to speaker attribution and is excluded from the strict total.

For certainty, **36 question answers were direct and unqualified**, while **5 response episodes used emphatic assurance or denial. These are different measures and overlap; they do not measure the speaker's actual knowledge or establish accuracy.

## The eight Public Safety follow-up commitments

| Time | Subject |
|---|---|
| 00:12:03 | Investigate congregating officers and report back; one episode despite multiple promises. |
| 00:13:21 | Check salary comparison and provide information. |
| 00:24:09 | Offer breakdown supporting line 214. |
| 00:25:25 | Provide parts/supplies spending and cost breakdown. |
| 00:32:32 | Get back on fiscal roles and reorganization. |
| 00:48:28 | Get back on skip tracer; three repeated promises count once. |
| 01:01:16 | Check whether 911 cost moved to or from capital. |
| 01:14:50 | Return with residency-requirement information after discussions. |

## Fire-specific finding

The closing fire discussion contains six spoken questions plus one request for PPE documentation. Public Safety directly answered two questions, partially addressed three, and gave an explanation without producing the requested PPE documentation. The Business Administrator answered the capital-budget follow-up. There is no explicit Public Safety promise to report back in this section; the council member asks Finance to reconcile the spending figures, which is not itself an accepted commitment. The fire-hose funding explanation remains unresolved in the transcript.

## Machine-readable count definitions

- **all_information_requests**: 111
- **spoken_substantive_questions**: 99
- **document_requests**: 12
- **follow_up_information_requests**: 78
- **follow_up_spoken_questions**: 68
- **follow_up_document_requests**: 10
- **PS_question_outcomes**: {'direct': 40, 'partial': 26, 'deferred': 5, 'unanswered': 2}
- **PS_all_request_outcomes**: {'direct': 41, 'partial': 27, 'deferred': 7, 'unanswered': 6}
- **PS_direct_answer_requests**: 41
- **PS_direct_answers_note**: Counted per information request resolved, not per sentence or unique speaker turn; some responses answer multiple prompts.
- **PS_partial_questions_including_mixed_replies**: 29
- **PS_unqualified_direct_question_answers**: 36
- **PS_explicit_follow_up_episodes**: 8
- **other_office_follow_up_episodes**: 6
- **uncertain_office_follow_up_episodes**: 1
- **PS_explicit_uncertainty_episodes**: 9
- **uncertain_attribution_uncertainty_episodes**: 1
- **PS_additional_hedged_episodes**: 11
- **PS_emphatic_certainty_episodes**: 5

## Counting rules and limitations

- Manual semantic coding of all 739 segments, not question-mark matching. These are analyst-coded counts of the supplied excerpt, not certified whole-hearing/video counts.
- A question is one distinct answerable information prompt. Requests phrased as explain/speak to/confirm and meaningful implied questions count. Multiple independent subquestions in one turn count separately; paraphrases of the same prompt before an answer count once. A repeated question after an inadequate answer counts again.
- Pure document/data-delivery requests are listed separately. All information requests equals substantive spoken questions plus document requests. Requests for permission to speak, audio checks, roll call, adjournment, officials clarifying what a council member means, rhetorical questions, and unaccepted policy suggestions are excluded.
- A follow-up develops a topic already raised in this excerpt, including a later council member following the earlier exchange. It does not automatically include a reference to a prior hearing. Follow-up is a subset, not an additional count.
- Direct means the response supplies the requested information or a definite yes/no/correction. Partial means relevant information without resolving the entire prompt. Deferred means checking or returning later is the primary disposition. Direct does not mean independently verified or correct.
- PS identifies Public Safety leadership/division presenters inferred from context. Finance, Business Administrator, council, and uncertain administrators are separately coded. No person-specific attribution is certified because the JSON has no speaker labels.
- Follow-up commitments count distinct topic-response episodes, not each repetition of get back to you. Promises to investigate count even if prompted by a service complaint rather than an information question. Hearing-order postponements, handoffs to a colleague currently present, document requests without assent, and internal future operational work do not count as promised follow-up to council.
- Explicit uncertainty includes stated inability to answer, needing to check factual alternatives, and clearly uncertain estimates. Additional hedge episodes include I believe, I think, to my knowledge, tentative recall, and visibly corrected estimates. Ordinary approximately/around alone does not count. One episode may combine hedged and explicit wording but is counted only in the explicit category.
- Certainty cannot be measured as a mental state. Unqualified direct question answers and emphatic certainty episodes are two different observable proxies. Emphatic certainty excludes promises such as definitely get back to you and ordinary yes/correct responses. These proxies must not be added together.
- The transcript begins mid-answer at 00:00:02. Opening questions and earlier presentation are absent. Several lines refer to August 6 and an upcoming August 21 despite the August 27 filename; this audit retains the supplied file label without independently establishing the meeting date.

## Question ledger

Q = spoken substantive question; D = document/data-delivery request. PS = Public Safety; other office assignments are contextual.

| ID | Time | Type | Follow-up | Prompt | Respondent | Result | Confidence |
|---|---|---|---|---|---|---|---|
| Q001 | 00:01:05 | Q | No | Is $1.5 million per year or spread over the grant term? | PS | direct | unqualified |
| Q002 | 00:02:42 | Q | Yes | What does the OEM grant offset include? | uncertain_admin | other_office | not_applicable |
| Q003 | 00:02:57 | Q | Yes | Is the grant money already in the budget separate from the litigated funds? | uncertain_admin | other_office | not_applicable |
| Q004 | 00:03:09 | Q | No | How much compensation does the range receive? | PS | partial | unqualified |
| Q005 | 00:03:09 | Q | No | How are the range receipts used? | PS | direct | unqualified |
| Q006 | 00:04:22 | Q | Yes | Does most or all range revenue return to that division? | PS | direct | unqualified |
| Q007 | 00:04:53 | Q | Yes | How much daily instruction do the three full-time instructors provide? | PS | partial | qualified |
| Q008 | 00:06:43 | Q | Yes | Does the range generate revenue in addition to meeting training requirements? | PS | direct | unqualified |
| Q009 | 00:07:51 | Q | Yes | How much did outside certification/training cost before the range opened? | PS | partial | unqualified |
| Q010 | 00:12:41 | Q | No | Why are Jersey City police salaries higher than Newark's? | PS | partial | qualified |
| Q011 | 00:13:14 | D | Yes | Review our salary comparison and get back to us. | PS | deferred | qualified |
| Q012 | 00:13:49 | Q | No | Explain the holiday and compensation-time line. | PS | deferred | unknown |
| Q013 | 00:15:03 | D | Yes | Provide where range revenue appears in the budget. | finance_BA | unanswered | not_applicable |
| Q014 | 00:15:25 | Q | Yes | What salary/administration amount is permitted under UASI? | PS | partial | unqualified |
| Q015 | 00:15:47 | Q | Yes | What is the grant's upper limit for salaries/administration, rather than the current salary? | PS | partial | unqualified |
| Q016 | 00:16:45 | Q | Yes | Is eligibility restricted to specific positions? | PS | direct | unqualified |
| Q017 | 00:16:50 | Q | Yes | Is there a dollar cap on the eligible salary? | PS | direct | unqualified |
| Q018 | 00:16:59 | D | Yes | Provide documentation of the salary cap and restrictions. | PS | unanswered | not_applicable |
| Q019 | 00:17:06 | Q | No | Explain the new communications line 302. | PS | direct | unqualified |
| Q020 | 00:18:47 | Q | Yes | By administration do you mean the federal administration? | PS | direct | unqualified |
| Q021 | 00:18:51 | Q | Yes | Is maintenance/repairs line 310 another formerly grant-funded expense? | PS | partial | unqualified |
| Q022 | 00:19:14 | Q | Yes | Is this maintenance for the range facility? | PS | direct | unqualified |
| Q023 | 00:20:02 | Q | Yes | Were the mobile-command expenses previously covered by UASI? | PS | direct | unqualified |
| Q024 | 00:20:22 | Q | Yes | Is the current city budget now covering those expenses? | PS | direct | unqualified |
| Q025 | 00:21:08 | Q | Yes | Does the communications funding pay for a contract? | PS | direct | unqualified |
| Q026 | 00:21:38 | Q | Yes | What is the $30,000 paying for given zero spending reported to date? | PS | partial | unqualified |
| Q027 | 00:22:31 | Q | Yes | Is there a contract for the wireless connectivity? | PS | direct | unqualified |
| Q028 | 00:22:43 | Q | Yes | Is that contract currently active? | PS | direct | unqualified |
| Q029 | 00:22:47 | D | Yes | Provide the contract and annual spending since 2022. | PS | unanswered | not_applicable |
| Q030 | 00:22:59 | Q | No | Explain the new $2,500 line 214 without a justification. | PS | direct | unqualified |
| Q031 | 00:23:50 | Q | Yes | Is it a new item or was it previously funded elsewhere? | PS | direct | unqualified |
| Q032 | 00:24:01 | D | Yes | Provide support/a breakdown for the request. | PS | deferred | unknown |
| Q033 | 00:24:38 | Q | No | Explain the parts-and-supplies increase given low expenditure. | PS_then_finance | partial | unqualified |
| Q034 | 00:25:55 | D | Yes | Provide copies/details of the open encumbrances. | PS | unanswered | not_applicable |
| Q035 | 00:26:10 | Q | Yes | Confirm video is not shared with immigration enforcement except under the specified judicial-warrant conditions. | PS | direct | unqualified |
| Q036 | 00:26:48 | Q | Yes | Confirm the salary offset is for UASI work involving seven counties. | PS | partial | qualified |
| Q037 | 00:28:00 | Q | Yes | Are Jersey City and Newark responsible for training the other jurisdictions? | PS | partial | qualified |
| Q038 | 00:29:29 | Q | Yes | Must someone be a current local employee to receive UASI compensation, or can a retiree participate? | PS | partial | unqualified |
| Q039 | 00:31:09 | Q | No | Explain the fiscal analyst's work and why OEM has this role when other divisions do not. | PS | partial | qualified |
| Q040 | 00:32:05 | Q | Yes | Should other divisions have analogous fiscal roles? | PS | deferred | unknown |
| Q041 | 00:33:24 | Q | No | Should the vehicle-audit inquiry go to OEM or DPW? | PS_then_BA | other_office | unknown |
| Q042 | 00:33:54 | Q | Yes | Will the citywide audit include vehicle and assignment details like the Public Safety spreadsheet? | finance_BA | other_office | not_applicable |
| Q043 | 00:34:47 | Q | No | How much revenue does parking enforcement generate? | PS | partial | qualified |
| Q044 | 00:35:29 | Q | No | How much additional revenue would another enforcement officer generate? | PS | partial | qualified |
| Q045 | 00:37:05 | Q | Yes | Who can provide the actual revenue figures: the division, Finance, or the court? | finance_BA | other_office | not_applicable |
| Q046 | 00:37:28 | Q | No | Explain the uniform allocation and low spending. | PS | direct | qualified |
| Q047 | 00:38:05 | Q | No | Are there encumbrances for that uniform line? | PS | partial | qualified |
| Q048 | 00:38:47 | Q | Yes | Are additional encumbrances anticipated? | PS | direct | unqualified |
| Q049 | 00:39:06 | Q | Yes | Have requisitions been submitted or are they still being prepared? | PS_then_finance | partial | unqualified |
| Q050 | 00:39:11 | D | Yes | Provide documentation of expected uniform amounts. | finance_BA | other_office | not_applicable |
| Q051 | 00:39:46 | Q | Yes | Are new uniforms being ordered where contractually required? | finance_BA | other_office | not_applicable |
| Q052 | 00:39:57 | Q | Yes | Will this year's uniform spending exceed last year's $57,000? | finance_BA | other_office | not_applicable |
| Q053 | 00:40:14 | D | Yes | Provide the uniform spending information when available. | finance_BA | other_office | not_applicable |
| Q054 | 00:40:57 | Q | No | To what extent can crossing guards cover events/construction instead of police overtime, and what limits apply? | PS | partial | unqualified |
| Q055 | 00:41:41 | Q | Yes | Is staffing the limitation on expanding that use? | PS | direct | unqualified |
| Q056 | 00:42:41 | Q | No | How many crossing-guard vacancies existed initially and how many remain? | PS | direct | unqualified |
| Q057 | 00:44:02 | Q | Yes | Why are crossing-guard jobs hard to fill: recruitment, advertising, or lack of interest? | PS | direct | unqualified |
| Q058 | 00:45:01 | Q | Yes | Can the city coordinate job fairs to recruit crossing guards? | finance_BA | other_office | not_applicable |
| Q059 | 00:48:04 | Q | No | What is the skip-tracer line/position? | PS | deferred | unknown |
| Q060 | 00:49:26 | Q | Yes | Does the skip tracer send people mail/how is the work performed? | council | other_office | not_applicable |
| Q061 | 00:50:27 | Q | No | Why was a third prosecutor not funded: revenue or recruiting constraints? | finance_BA | other_office | not_applicable |
| Q062 | 00:51:30 | Q | Yes | Are additional prosecutor positions therefore a longer-term goal? | finance_BA | other_office | not_applicable |
| Q063 | 00:51:42 | Q | Yes | Why fund a vacant chief prosecutor position while there is an acting chief? | finance_BA | other_office | not_applicable |
| Q064 | 00:53:07 | Q | Yes | Would the administration agree to remove the proposed prosecutor allocations for savings? | finance_BA | other_office | not_applicable |
| Q065 | 00:53:40 | Q | Yes | Are the municipal prosecutors full-time or part-time? | council | other_office | not_applicable |
| Q066 | 00:54:48 | Q | Yes | Again, are the full-time budget lines actually full-time staff? | finance_BA | other_office | not_applicable |
| Q067 | 00:54:48 | Q | Yes | Do those prosecutors work for you? | uncertain_admin | unanswered | not_applicable |
| Q068 | 00:55:12 | Q | No | Does RC fall under Quality of Life? | uncertain_admin | other_office | not_applicable |
| Q069 | 00:55:18 | Q | Yes | Where are the RC positions in the budget workbook? | uncertain_admin | other_office | not_applicable |
| Q070 | 00:55:41 | Q | No | Explain the printing/advertising line and its expenditure. | PS | partial | unqualified |
| Q071 | 00:56:02 | Q | No | Are encumbrances forthcoming for printing/advertising? | PS_then_finance | partial | unknown |
| Q072 | 00:57:03 | Q | Yes | Who prints the law books/how are they obtained? | finance_BA | other_office | not_applicable |
| Q073 | 00:57:26 | Q | Yes | Do the vendors print the books for the division? | finance_BA | other_office | not_applicable |
| Q074 | 00:57:30 | Q | Yes | Why are purchased books charged to printing and advertising? | finance_BA | other_office | not_applicable |
| Q075 | 00:57:52 | Q | Yes | How much is spent annually on law books? | finance_BA | other_office | not_applicable |
| Q076 | 00:59:21 | Q | No | Explain the contracts under line 314. | PS | direct | unqualified |
| Q077 | 01:00:02 | D | Yes | Was the contract/value list sent, and can council obtain it? | PS | direct | qualified |
| Q078 | 01:00:35 | Q | Yes | What was shifted between operating and capital funding? | PS | direct | qualified |
| Q079 | 01:01:02 | Q | Yes | Was it shifted to capital or from capital as the note says? | PS | deferred | unknown |
| Q080 | 01:01:48 | Q | No | Provide the rank breakdown of officers who left since January. | PS | direct | qualified |
| Q081 | 01:02:17 | Q | Yes | How many departing officers were lieutenants? | PS | direct | unqualified |
| Q082 | 01:02:34 | Q | Yes | Were the three additional departures all police officers? | PS | direct | unqualified |
| Q083 | 01:02:42 | Q | No | What was the impact of losing two deputy chiefs and how was the division reorganized? | PS | direct | unqualified |
| Q084 | 01:06:52 | Q | Yes | Can captains fill those responsibilities? | PS | direct | unqualified |
| Q085 | 01:07:06 | Q | No | How would a roughly $3 million reduction require closing districts? | PS | direct | unqualified |
| Q086 | 01:11:30 | Q | Yes | How many deputy chiefs does Newark currently have? | PS | direct | qualified |
| Q087 | 01:12:37 | Q | Yes | Could deputy chiefs be moved to captain roles now without layoffs? | PS | partial | unqualified |
| Q088 | 01:12:53 | Q | Yes | How many captains are there currently? | PS | unanswered | not_applicable |
| Q089 | 01:12:53 | Q | Yes | How many captain positions are available in the organization chart? | PS | unanswered | not_applicable |
| Q090 | 01:13:29 | Q | Yes | Again, how many captain positions are in the organization chart? | PS | partial | unqualified |
| Q091 | 01:13:38 | Q | Yes | Are there open captain positions? | PS | partial | unknown |
| Q092 | 01:14:06 | Q | Yes | Is fewer deputies and more captains the intended direction here too? | PS | direct | unqualified |
| Q093 | 01:14:27 | Q | No | Might you recommend suspending the residency requirement for new hires? | PS | deferred | unknown |
| Q094 | 01:15:29 | Q | No | Give an update on Class II special officers as a staffing/cost option. | PS | direct | unqualified |
| Q095 | 01:16:41 | Q | Yes | Is a deputy chief assigned to municipal court? | PS | direct | unqualified |
| Q096 | 01:17:09 | Q | No | Does a significant share of sworn overtime go to superior officers? | PS | partial | qualified |
| Q097 | 01:17:46 | Q | Yes | Is that overtime for lieutenants covering captain roles? | PS | direct | unqualified |
| Q098 | 01:17:53 | Q | Yes | Is the contractual higher-rank threshold eight hours? | PS | partial | unqualified |
| Q099 | 01:18:39 | D | No | Provide documentation for expense lines 203, 208, and 214. | PS | unanswered | not_applicable |
| Q100 | 01:18:58 | D | Yes | Provide current rank counts instead of the June 30 workbook figures. | finance_BA | other_office | not_applicable |
| Q101 | 01:20:32 | Q | Yes | Does the police officer count include incoming academy classes? | PS | direct | unqualified |
| Q102 | 01:20:58 | Q | Yes | Is there another academy class coming? | PS | direct | unqualified |
| Q103 | 01:22:27 | Q | Yes | How many sworn officers are there now? | PS | direct | unqualified |
| Q104 | 01:23:09 | Q | Yes | How many are physically available to work after leave and retirement-related absences? | PS | partial | unqualified |
| Q105 | 01:25:00 | Q | No | Explain the removed vehicle-leasing and fire-hose lines and their replacement funding. | PS | partial | unqualified |
| Q106 | 01:25:42 | Q | No | What is the apparatus replacement plan and will it appear in capital funding? | PS | partial | unqualified |
| Q107 | 01:27:25 | Q | Yes | Can council expect apparatus in the capital budget? | finance_BA | other_office | not_applicable |
| Q108 | 01:28:07 | D | No | Provide documentation and encumbrances for firefighter gear line 215. | PS | partial | qualified |
| Q109 | 01:29:46 | Q | Yes | Did you say $1.3 million was spent last year? | PS | direct | unqualified |
| Q110 | 01:30:08 | Q | Yes | Reconcile that with Finance showing about $424,000 for calendar 2025. | PS | partial | unqualified |
| Q111 | 01:30:57 | Q | No | Clarify on the record whether there were plans to close two fire companies/firehouses. | PS | direct | unqualified |

## Follow-up, uncertainty and certainty episodes

| ID | Time | Category | Office | Interpretation |
|---|---|---|---|---|
| E001 | 00:12:03 | follow_up | PS | Investigate congregating officers and report back; one episode despite multiple promises. |
| E002 | 00:13:21 | follow_up | PS | Check salary comparison and provide information. |
| E003 | 00:24:09 | follow_up | PS | Offer breakdown supporting line 214. |
| E004 | 00:25:25 | follow_up | PS | Provide parts/supplies spending and cost breakdown. |
| E005 | 00:32:32 | follow_up | PS | Get back on fiscal roles and reorganization. |
| E006 | 00:48:28 | follow_up | PS | Get back on skip tracer; three repeated promises count once. |
| E007 | 01:01:16 | follow_up | PS | Check whether 911 cost moved to or from capital. |
| E008 | 01:14:50 | follow_up | PS | Return with residency-requirement information after discussions. |
| E009 | 00:02:34 | follow_up | uncertain_admin | Circle back with Finance about including grant funding; likely administration, attribution not secure. |
| E010 | 00:37:17 | follow_up | finance_BA | Add parking revenue to the information requests. |
| E011 | 00:40:14 | follow_up | finance_BA | Provide uniform information when ready. |
| E012 | 00:52:24 | follow_up | finance_BA | Circle back on chief prosecutor budget line. |
| E013 | 00:56:52 | follow_up | finance_BA | Provide updated expenditure report. |
| E014 | 00:57:55 | follow_up | finance_BA | Find book expenditure and provide request when received. |
| E015 | 01:19:57 | follow_up | finance_BA | Update/send current rank counts. |
| E016 | 00:01:25 | uncertainty_explicit | PS | Not quite sure why litigation is holding up the grant. |
| E017 | 00:12:14 | uncertainty_explicit | PS | Does not know why officers were congregating; facts still needed. |
| E018 | 00:18:35 | uncertainty_explicit | PS | Does not know why federal grant guidance changed. |
| E019 | 00:31:58 | uncertainty_explicit | PS | Does not know whether fiscal analyst is the correct title. |
| E020 | 00:33:41 | uncertainty_explicit | PS_then_BA | I cannot answer that question, followed by vehicle audit answer from administration; speaker boundary uncertain. |
| E021 | 00:48:28 | uncertainty_explicit | PS | Mistakes skip tracer for software, corrects to position, cannot explain without checking. |
| E022 | 00:56:19 | uncertainty_explicit | PS | Unable to say whether Quality of Life has open encumbrances. |
| E023 | 01:00:50 | uncertainty_explicit | PS | Unsure whether cost shifted to or from capital; will check. |
| E024 | 01:12:03 | uncertainty_explicit | PS | Newark deputy count could be five/six working or eight on payroll. |
| E025 | 01:17:27 | uncertainty_explicit | PS | Does not know the superior-officer share of overtime before giving estimates. |
| E026 | 00:00:20 | uncertainty_hedge | PS | I believe the original grant was $312,000. |
| E027 | 00:05:37 | uncertainty_hedge | PS | Qualification cycle: three months, then six months/chief consultation. |
| E028 | 00:13:02 | uncertainty_hedge | PS | I do not think so / I believe Newark salary is higher. |
| E029 | 00:27:14 | uncertainty_hedge | PS | Might miss a county in the list. |
| E030 | 00:28:32 | uncertainty_hedge | PS | I want to say close to $24 million. |
| E031 | 00:29:04 | uncertainty_hedge | PS | Meeting date: I believe August 21. |
| E032 | 00:38:35 | uncertainty_hedge | PS | To my knowledge, uniform spending or encumbrance exceeded 100. |
| E033 | 01:00:08 | uncertainty_hedge | PS | I believe the contract list was sent. |
| E034 | 01:02:08 | uncertainty_hedge | PS | I believe, when recalling departing ranks. |
| E035 | 01:04:30 | uncertainty_hedge | PS | I believe the former deputy office was on Marian. |
| E036 | 01:29:04 | uncertainty_hedge | PS | I believe annual PPE contract estimate was $1.5 million. |
| E037 | 00:02:18 | certainty_explicit | PS | I am quite sure training can be paid through the grant. |
| E038 | 00:26:35 | certainty_explicit | PS | Repeatedly affirms full compliance and no information sharing. |
| E039 | 00:38:20 | certainty_explicit | PS | We definitely have to provide crossing-guard uniforms; contractual. |
| E040 | 01:18:27 | certainty_explicit | PS | Definitely need lieutenants; budgeted openings can save overtime. |
| E041 | 01:31:20 | certainty_explicit | PS | Emphatic never denial of a stated firehouse-closure plan. |
