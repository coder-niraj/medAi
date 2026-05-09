# Med AI

The platform is purpose-built for the MENA region, with full RTL Arabic language support, compliance with Saudi Arabia's
PDPL and the UAE Federal Decree-Law No. 45 of 2021, and data residency within Google Cloud's Dammam region (mecentral2) for KSA patients


## API Reference

### Auth 

#### Register

```http
  POST /auth/register
```

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `firebase_id_token` | `string` | **Required**.  |
| `name` | `string` | **Required**.|
| `phone` | `string` | **Required**.|
| `dob` | `string` | **Required**.|



###
#### Login

```http
  POST /auth/login
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `firebase_id_token`      | `string` | **Required** |

**rate limit:**  10 failed/hr | 60 req/min

###
#### Consent

```http
  POST /auth/consent
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `tos_accepted`      | `bool` | **Required**. |
| `research_consent`      | `bool` | **Required**.


###
#### Guest Consent

```http
  POST /auth/guest-consent
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `tos_accepted`      | `bool` | **Required**.  |
| `research_consent`      | `bool` | **Required**.  |
| `age_range`      | `string` | **Required**.  |
| `gender`      | `string` | **Required**.  |
| `nationality`      | `string` | **Required**.  |

**rate limit:**  60 req/min | 1 guest/device+IP/24hr

### Reports

 #### Upload Documents

```http
  POST /reports/upload
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `header-auth-token`      | `string` | **Required**. |
| `file`      | `file` | **Required**. |
| `report_type`      | `string` | **Required**. |
| `display_name`      | `string` | **Required**. |

**rate limit:**  5 uploads/day | 60 req/min | X-Idempotency-Key
 
 `1-hour TTL. Prevents duplicate uploads from flaky mobile connections.`
###
 #### List Of Reports

```http
  GET /reports
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `header-auth-token`      | `string` | **Required**. |

###
#### AI Report Summary

```http
  GET /reports/{report_id}/summary
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `report_id`      | `string` | **Required**. id of report in url |
| `header-auth-token`      | `string` | **Required**. |


###
#### Accesible Limited Time URL

```http
  GET /reports/{report_id}/file
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `report_id`      | `string` | **Required**. id of report in url |
| `header-auth-token`      | `string` | **Required**. |


###
 #### Delete Report

```http
  DELETE /reports/{report_id}
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `report_id`      | `string` | **Required**. id of report in url |
| `header-auth-token`      | `string` | **Required**. |



### Chat

 #### Create Chat Session

```http
  POST /chat/sessions
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `header-auth-token`      | `string` | **Required**. |
| `report_id`      | `string` | **Required**. id of report |
| `mode`      | `Enum` | document - general - triage |

**rate limit:**  60 req/min | 1 guest/device+IP/24hr
###
 #### List All Sessions

```http
  GET /chat/sessions
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `header-auth-token`      | `string` | **Required**. |
| `mode (optional)`      | `Enum` | document - general - triage. |
| `limit`      | `int` | 20 |

###
 #### Send Chat Message

```http
  POST /chat/sessions/{session_id}/messages
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `header-auth-token`      | `string` | **Required**. |
| `session_id`      | `string` | **Required**. id of session in url |
| `message`      | `string` | **Required**.  |

**rate limit:**  10 msg/min
###
 #### Retrive Chat Session History

```http
  GET /chat/sessions/{session_id}/messages
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `header-auth-token`      | `string` | **Required**. |
| `session_id`      | `string` | **Required**. id of session in url |


### Triage

 #### Trigger Triage Result Generation

```http
  POST /triage/complete/{session_id}
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `header-auth-token`      | `string` | **Required**. |
| `session_id`      | `string` | **Required**. id of session in url |

**rate limit:**  60 req/min | X-Idempotency-Key

###
 #### Link Guest Triage To Newly registered User

```http
  POST /triage/claim
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `header-guest-token`      | `string` | **Required**. |
| `guest_token`      | `string` | **Required**. token id of guest |
###
 #### Retrive Specific Triage Result

```http
  GET /triage/results/{triage_result_id}
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `header-auth-token`      | `string` | **Required**. |
| `triage_result_id`      | `string` | **Required**. Id of triage |
###
 #### List All Triage Results

```http
  GET /triage/results
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `header-auth-token`      | `string` | **Required**. |

###
 #### Rating And FeedBack

```http
  Patch /chat/sessions/{session_id}/messages/{message_id}/feedback
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `rating`      | `int` | **Required**.|
| `flag`      | `Enum` | helpful - wrong - unsafe - too_vague|
| `header-auth-token`      | `string` | **Required**.|
###

### User

 #### Export All Data for Authenticated User

```http
  GET /users/me/data-export
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `header-auth-token`      | `string` | **Required**.|
###

 #### Delete Entire Patient Account

```http
  DELETE /users/me
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `header-auth-token`      | `string` | **Required**.|
###

### Internal (Admin Only)

 #### Triogger Nightly PipeLine

```http
  POST /internal/ft-pipeline/run
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `header-admin-token`      | `string` | **Required**.|
###


 #### Fine Tuning Dataset Health Check

```http
  GET /internal/ft-pipeline/stats
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `header-admin-token`      | `string` | **Required**.|
###


### Health Status + LLM Traces Endpoints

 #### Service Health Status

```http
  GET /health
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `header-auth-token`      | `string` | **Required**.|
###


 #### LLM Traces 

```http
  GET /internal/traces/{message_id}
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `message_id`      | `string` | **Required**. id of message in url|
| `header-auth-token`      | `string` | **Required**. only for docter and admin|
###
