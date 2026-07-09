# DPDP Compliance Summary

## Consent

Users are informed that their audio files will be processed to generate pronunciation feedback. The upload flow should display a simple consent notice before assessment begins.

## Purpose Limitation

The application uses the uploaded audio solely for pronunciation assessment and feedback generation. The system does not use the recording for any unrelated purpose.

## Temporary Audio Processing

Audio files are accepted temporarily for analysis and are deleted immediately after the assessment completes. No permanent storage is required for the core workflow.

## Encryption in Transit

All requests should be sent over HTTPS in production. The frontend and backend are designed for secure deployment with HTTPS enabled.

## Immediate Deletion After Processing

The backend removes temporary audio files after the response is generated. In production, the deployment should also enforce short-lived temporary storage and access control.

## No Permanent Storage

The application does not create user accounts or maintain a persistent audio archive. The assessment output is returned as JSON and displayed to the user.

## Data Retention Policy

No long-term retention is required for the main workflow. Temporary files are deleted as soon as the analysis completes.

## Deletion Policy

If a deployment needs to support retention logs, those logs should be short-lived and restricted to operational purposes only. Audio payloads should not be retained beyond the processing window.

## Cross-Border Processing Considerations

If the service routes data to third-party providers such as Azure or OpenAI, the deployment should ensure that the selected region and data handling terms align with the organization’s compliance policy.

## Compliance with India’s Digital Personal Data Protection Act, 2023

The application follows the core principles of the DPDP Act by limiting collection and processing to the minimum necessary data, using temporary processing, avoiding account-based storage, and communicating clear purpose and deletion expectations.
