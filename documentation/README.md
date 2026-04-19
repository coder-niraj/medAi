
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
| `api_key` | `string` | **Required**. Your API key |

###
#### Login

```http
  POST /auth/login
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `id`      | `string` | **Required**. Id of item to fetch |


###
#### Consent

```http
  POST /auth/consent
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `id`      | `string` | **Required**. Id of item to fetch |


###
#### Guest Consent

```http
  POST /auth/guest-consent
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `id`      | `string` | **Required**. Id of item to fetch |



### Reports

 #### Upload Documents

```http
  POST /reports/upload
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `id`      | `string` | **Required**. Id of item to fetch |

###
 #### List Of Reports

```http
  GET /reports
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `id`      | `string` | **Required**. Id of item to fetch |

###
#### AI Report Summary

```http
  GET /reports/{report_id}/summary
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `id`      | `string` | **Required**. Id of item to fetch |

###
#### Accesible Limited Time URL

```http
  GET /reports/{report_id}/file
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `id`      | `string` | **Required**. Id of item to fetch |

###
 #### Delete Report

```http
  DELETE /reports/{report_id}
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `id`      | `string` | **Required**. Id of item to fetch |


### Chat

 #### Create Chat Session

```http
  POST /chat/sessions
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `id`      | `string` | **Required**. Id of item to fetch |
###
 #### List All Sessions

```http
  GET /chat/sessions
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `id`      | `string` | **Required**. Id of item to fetch |

###
 #### Send Chat Message

```http
  POST /chat/sessions/{session_id}/messages
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `id`      | `string` | **Required**. Id of item to fetch |

###
 #### Retrive Chat Session History

```http
  GET /chat/sessions/{session_id}/messages
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `id`      | `string` | **Required**. Id of item to fetch |


### Triage

 #### Trigger Triage Result Generation

```http
  POST /triage/complete/{session_id}
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `id`      | `string` | **Required**. Id of item to fetch |
###
 #### Link Guest Triage To Newly registered User

```http
  POST /triage/claim
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `id`      | `string` | **Required**. Id of item to fetch |
###
 #### Retrive Specific Triage Result

```http
  GET /triage/results/{triage_result_id}
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `id`      | `string` | **Required**. Id of item to fetch |
###
 #### List All Triage Results

```http
  GET /triage/results
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `id`      | `string` | **Required**. Id of item to fetch |
###
 #### Rating And FeedBack

```http
  Patch /chat/sessions/{session_id}/messages/{message_id}/feedback
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `id`      | `string` | **Required**. Id of item to fetch |
###

### User

 #### Export All Data for Authenticated User

```http
  GET /users/me/data-export
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `id`      | `string` | **Required**. Id of item to fetch |
###

 #### Delete Entire Patient Account

```http
  DELETE /users/me
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `id`      | `string` | **Required**. Id of item to fetch |
###

### Internal (Admin Only)

 #### Triogger Nightly PipeLine

```http
  POST /internal/ft-pipeline/run
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `id`      | `string` | **Required**. Id of item to fetch |
###


 #### Fine Tuning Dataset Health Check

```http
  GET /internal/ft-pipeline/stats
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `id`      | `string` | **Required**. Id of item to fetch |
###


### Health Status + LLM Traces Endpoints

 #### Service Health Status

```http
  GET /health
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `id`      | `string` | **Required**. Id of item to fetch |
###


 #### LLM Traces 

```http
  GET /internal/traces/{message_id}
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `id`      | `string` | **Required**. Id of item to fetch |
###