# HABET-CircuitPython-Payloads
A repository for HABET standard payload CircuitPython scripts.

These scripts have been cleaned of the clutter inlcuded in the original versions.

Tracking Payload: Basic format for a payload that just transmits GPS data.

Customer Payload: Basic format for a payload that transmits GPS data and external payload data connected via UART. Supports two external payloads on separate uart lines. HABET paylaod sends "Ready" to the payload to indicate it is prepared to recieve data. It can recieve up to 241 bytes and then transmits that with a label indicating which payload the data is from.