# Instructions

- Following Playwright test failed.
- Explain why, be concise, respect Playwright best practices.
- Provide a snippet of code with the fix, if possible.

# Test info

- Name: insurance-billing/coverage.spec.ts >> Coverage — Accepted Insurance Plans >> 1-char name → at least 2 characters error
- Location: tests/insurance-billing/coverage.spec.ts:72:7

# Error details

```
TypeError: insuranceBilling.smartFill is not a function
```

# Page snapshot

```yaml
- generic [ref=e4]:
  - complementary [ref=e5]:
    - img "DentalBase Logo" [ref=e7]
    - navigation [ref=e8]:
      - link "Overview" [ref=e9] [cursor=pointer]:
        - /url: /overview
      - link "Calls" [ref=e15] [cursor=pointer]:
        - /url: /calls
      - link "Patients" [ref=e20] [cursor=pointer]:
        - /url: /patients
      - link "Messages" [ref=e26] [cursor=pointer]:
        - /url: /messages
      - link "Tasks" [ref=e29] [cursor=pointer]:
        - /url: /tasks
      - link "Schedule" [ref=e33] [cursor=pointer]:
        - /url: /schedule
      - link "Forms" [ref=e36] [cursor=pointer]:
        - /url: /forms
      - link "Reviews" [ref=e40] [cursor=pointer]:
        - /url: /reviews
      - link "Patient Outreach" [ref=e43] [cursor=pointer]:
        - /url: /patient-outreach
      - link "Settings" [ref=e48] [cursor=pointer]:
        - /url: /settings
      - button "Phone System" [ref=e52] [cursor=pointer]
    - generic [ref=e55]:
      - button "Collapse" [ref=e56] [cursor=pointer]
      - generic [ref=e60]:
        - img "User" [ref=e61]
        - generic:
          - generic [ref=e62]:
            - paragraph [ref=e63]: Reem Sibakhi
            - paragraph [ref=e64]: User
          - button "Logout" [ref=e65]
  - generic [ref=e69]:
    - banner [ref=e70]:
      - textbox "Search patients..." [ref=e75]
      - generic [ref=e76]:
        - button [ref=e77] [cursor=pointer]
        - button "Softphone" [ref=e81] [cursor=pointer]
        - button "100+" [ref=e87] [cursor=pointer]
        - button "Logout" [ref=e92] [cursor=pointer]
    - main [ref=e96]:
      - generic [ref=e98]:
        - generic [ref=e99]:
          - heading "Settings" [level=3] [ref=e100]
          - generic [ref=e104]: "Office: Smile Dental"
        - generic [ref=e105]:
          - navigation [ref=e107]:
            - button "Profile" [ref=e108] [cursor=pointer]
            - button "Practice Profile & Hours" [ref=e109] [cursor=pointer]
            - button "Scheduling Rules" [ref=e110] [cursor=pointer]
            - button "Patient Outreach" [ref=e111] [cursor=pointer]
            - button "DentiVoice™ Customization" [ref=e112] [cursor=pointer]
            - button "Insurance & Billing" [ref=e113] [cursor=pointer]
            - button "Office Setup" [ref=e114] [cursor=pointer]
          - generic [ref=e117]:
            - generic [ref=e119]:
              - generic [ref=e120]:
                - generic [ref=e121]:
                  - heading "Coverage" [level=3] [ref=e122]
                  - paragraph [ref=e123]: Insurance acceptance policy
                - generic [ref=e124]: All Insurance Accepted
                - button "Edit" [ref=e128] [cursor=pointer]
              - generic [ref=e132]:
                - generic [ref=e133]:
                  - heading "Membership Plans" [level=3] [ref=e134]
                  - paragraph [ref=e135]: 5 membership plans
                - generic [ref=e137]:
                  - generic [ref=e138]:
                    - generic [ref=e139]:
                      - paragraph [ref=e140]: Individual Adult Plan
                      - paragraph [ref=e141]: custom • 20% discount
                    - generic [ref=e142]:
                      - paragraph [ref=e143]: $399/yr
                      - paragraph [ref=e144]: $35/mo
                  - generic [ref=e145]:
                    - generic [ref=e146]:
                      - paragraph [ref=e147]: Family Plan
                      - paragraph [ref=e148]: individual • 20% discount
                    - generic [ref=e149]:
                      - paragraph [ref=e150]: $899/yr
                      - paragraph [ref=e151]: $80/mo
                  - generic [ref=e152]:
                    - generic [ref=e153]:
                      - paragraph [ref=e154]: Senior Plan (65+)
                      - paragraph [ref=e155]: senior • 15% discount
                    - generic [ref=e156]:
                      - paragraph [ref=e157]: $279/yr
                      - paragraph [ref=e158]: $25/mo
                  - button "+2 more" [ref=e159] [cursor=pointer]
                - button "Edit" [ref=e161] [cursor=pointer]
              - generic [ref=e165]:
                - generic [ref=e166]:
                  - heading "Finance" [level=3] [ref=e167]
                  - paragraph [ref=e168]: Payment financing options
                - generic [ref=e169]: 0 providers
                - button "Edit" [ref=e173] [cursor=pointer]
              - generic [ref=e177]:
                - generic [ref=e178]:
                  - heading "Service Pricing" [level=3] [ref=e179]
                  - paragraph [ref=e180]: Service pricing
                - generic [ref=e183]:
                  - generic [ref=e184]: preventive
                  - generic [ref=e185]: "2"
                - button "Edit" [ref=e187] [cursor=pointer]
              - generic [ref=e191]:
                - generic [ref=e192]:
                  - heading "Active Offers" [level=3] [ref=e193]
                  - paragraph [ref=e194]: 1 promotions
                - generic [ref=e197]:
                  - generic [ref=e198]:
                    - paragraph [ref=e199]: ds
                    - paragraph [ref=e200]: all patients
                  - generic [ref=e201]: $1
                - button "Edit" [ref=e203] [cursor=pointer]
              - generic [ref=e207]:
                - generic [ref=e208]:
                  - heading "Pricing Policy" [level=3] [ref=e209]
                  - paragraph [ref=e210]: Disclosure and discounts
                - generic [ref=e211]: Always provide exact pricing
                - button "Edit" [ref=e213] [cursor=pointer]
            - dialog "Accepted Insurance Plans" [ref=e218]:
              - generic [ref=e219]:
                - generic [ref=e221]:
                  - generic [ref=e225]:
                    - heading "Accepted Insurance Plans" [level=2] [ref=e226]
                    - paragraph [ref=e227]: Configure which insurance providers your practice accepts
                  - button "Close panel" [ref=e228] [cursor=pointer]
                - generic [ref=e232]:
                  - generic [ref=e233]:
                    - generic [ref=e234]:
                      - generic [ref=e235]: Accept All Insurance
                      - paragraph [ref=e237]: Accept any insurance plan patients may have
                    - switch "Accept All Insurance" [checked] [ref=e239] [cursor=pointer]
                  - generic [ref=e240]:
                    - text: Quick Add Major Providers
                    - generic [ref=e241]:
                      - button "✓ Delta Dental" [ref=e242] [cursor=pointer]
                      - button "✓ MetLife" [ref=e243] [cursor=pointer]
                      - button "✓ Cigna Dental" [ref=e244] [cursor=pointer]
                      - button "✓ Aetna Dental" [ref=e245] [cursor=pointer]
                      - button "✓ Guardian" [ref=e246] [cursor=pointer]
                      - button "✓ Humana Dental" [ref=e247] [cursor=pointer]
                      - button "✓ United Healthcare" [ref=e248] [cursor=pointer]
                      - button "✓ Anthem BlueCross" [ref=e249] [cursor=pointer]
                      - button "✓ United Concordia" [ref=e250] [cursor=pointer]
                      - button "✓ Ameritas" [ref=e251] [cursor=pointer]
                      - button "✓ Principal" [ref=e252] [cursor=pointer]
                      - button "✓ GEHA" [ref=e253] [cursor=pointer]
                  - generic [ref=e254]:
                    - generic [ref=e255]:
                      - generic [ref=e256]: Accepted Plans
                      - button "Add Custom" [active] [ref=e257] [cursor=pointer]
                    - generic [ref=e259]:
                      - generic [ref=e260]:
                        - generic [ref=e261]: New Plan
                        - button [ref=e262]
                      - generic [ref=e266]:
                        - generic [ref=e267]:
                          - generic [ref=e269]:
                            - text: Insurance Name
                            - generic [ref=e270]: "*"
                          - textbox "Insurance Name" [ref=e272]
                        - generic [ref=e273]:
                          - generic [ref=e275]:
                            - text: Payer ID
                            - generic [ref=e276]: "*"
                          - textbox "Payer ID" [ref=e278]
                      - generic [ref=e279]:
                        - generic [ref=e280]:
                          - generic [ref=e281]: Plan Type
                          - combobox "Plan Type" [ref=e284] [cursor=pointer]:
                            - generic: PPO
                        - generic [ref=e287]:
                          - generic [ref=e288]: Network Status
                          - combobox "Network Status" [ref=e291] [cursor=pointer]:
                            - generic: In-Network
                      - generic [ref=e294]:
                        - generic [ref=e295]: Coverage %
                        - generic [ref=e296]:
                          - generic [ref=e297]:
                            - generic [ref=e298]: Preventive
                            - spinbutton "Preventive" [ref=e301]: "100"
                          - generic [ref=e302]:
                            - generic [ref=e303]: Basic
                            - spinbutton "Basic" [ref=e306]: "80"
                          - generic [ref=e307]:
                            - generic [ref=e308]: Major
                            - spinbutton "Major" [ref=e311]: "50"
                      - generic [ref=e312]:
                        - generic [ref=e313]: Orthodontic Coverage (%)
                        - spinbutton "Orthodontic Coverage (%)" [ref=e316]: "50"
                      - generic [ref=e317]:
                        - button "Cancel" [ref=e318] [cursor=pointer]
                        - button "Save Plan" [disabled] [ref=e319]
                    - generic [ref=e320]:
                      - generic [ref=e322]:
                        - generic [ref=e323] [cursor=pointer]:
                          - paragraph [ref=e324]: Delta Dental
                          - generic [ref=e325]: in-network
                        - generic [ref=e326]:
                          - switch [checked] [ref=e327] [cursor=pointer]
                          - button [ref=e328] [cursor=pointer]
                      - generic [ref=e332]:
                        - generic [ref=e333] [cursor=pointer]:
                          - paragraph [ref=e334]: MetLife
                          - generic [ref=e335]: in-network
                        - generic [ref=e336]:
                          - switch [checked] [ref=e337] [cursor=pointer]
                          - button [ref=e338] [cursor=pointer]
                      - generic [ref=e342]:
                        - generic [ref=e343] [cursor=pointer]:
                          - paragraph [ref=e344]: Cigna Dental
                          - generic [ref=e345]: in-network
                        - generic [ref=e346]:
                          - switch [checked] [ref=e347] [cursor=pointer]
                          - button [ref=e348] [cursor=pointer]
                      - generic [ref=e352]:
                        - generic [ref=e353] [cursor=pointer]:
                          - paragraph [ref=e354]: Aetna Dental
                          - generic [ref=e355]: in-network
                        - generic [ref=e356]:
                          - switch [checked] [ref=e357] [cursor=pointer]
                          - button [ref=e358] [cursor=pointer]
                      - generic [ref=e362]:
                        - generic [ref=e363] [cursor=pointer]:
                          - paragraph [ref=e364]: Guardian
                          - generic [ref=e365]: in-network
                        - generic [ref=e366]:
                          - switch [checked] [ref=e367] [cursor=pointer]
                          - button [ref=e368] [cursor=pointer]
                      - generic [ref=e372]:
                        - generic [ref=e373] [cursor=pointer]:
                          - paragraph [ref=e374]: Humana Dental
                          - generic [ref=e375]: in-network
                        - generic [ref=e376]:
                          - switch [checked] [ref=e377] [cursor=pointer]
                          - button [ref=e378] [cursor=pointer]
                      - generic [ref=e382]:
                        - generic [ref=e383] [cursor=pointer]:
                          - paragraph [ref=e384]: United Healthcare
                          - generic [ref=e385]: in-network
                        - generic [ref=e386]:
                          - switch [checked] [ref=e387] [cursor=pointer]
                          - button [ref=e388] [cursor=pointer]
                      - generic [ref=e392]:
                        - generic [ref=e393] [cursor=pointer]:
                          - paragraph [ref=e394]: Anthem BlueCross
                          - generic [ref=e395]: in-network
                        - generic [ref=e396]:
                          - switch [checked] [ref=e397] [cursor=pointer]
                          - button [ref=e398] [cursor=pointer]
                      - generic [ref=e402]:
                        - generic [ref=e403] [cursor=pointer]:
                          - paragraph [ref=e404]: United Concordia
                          - generic [ref=e405]: in-network
                        - generic [ref=e406]:
                          - switch [checked] [ref=e407] [cursor=pointer]
                          - button [ref=e408] [cursor=pointer]
                      - generic [ref=e412]:
                        - generic [ref=e413] [cursor=pointer]:
                          - paragraph [ref=e414]: Ameritas
                          - generic [ref=e415]: in-network
                        - generic [ref=e416]:
                          - switch [checked] [ref=e417] [cursor=pointer]
                          - button [ref=e418] [cursor=pointer]
                      - generic [ref=e422]:
                        - generic [ref=e423] [cursor=pointer]:
                          - paragraph [ref=e424]: Principal
                          - generic [ref=e425]: in-network
                        - generic [ref=e426]:
                          - switch [checked] [ref=e427] [cursor=pointer]
                          - button [ref=e428] [cursor=pointer]
                      - generic [ref=e432]:
                        - generic [ref=e433] [cursor=pointer]:
                          - paragraph [ref=e434]: GEHA
                          - generic [ref=e435]: in-network
                        - generic [ref=e436]:
                          - switch [checked] [ref=e437] [cursor=pointer]
                          - button [ref=e438] [cursor=pointer]
                      - generic [ref=e442]:
                        - generic [ref=e443] [cursor=pointer]:
                          - paragraph [ref=e444]: Delta_ms4csbxf_b0a
                          - generic [ref=e445]: in-network
                        - button [ref=e447] [cursor=pointer]
                      - generic [ref=e451]:
                        - generic [ref=e452] [cursor=pointer]:
                          - paragraph [ref=e453]: Delta_ms4cve7v_2od
                          - generic [ref=e454]: in-network
                        - button [ref=e456] [cursor=pointer]
                      - generic [ref=e460]:
                        - generic [ref=e461] [cursor=pointer]:
                          - paragraph [ref=e462]: Delta_ms4cwa18_5k0
                          - generic [ref=e463]: in-network
                        - button [ref=e465] [cursor=pointer]
                  - generic [ref=e469]:
                    - generic [ref=e470]: Additional Notes
                    - generic [ref=e472]:
                      - textbox "Additional Notes" [ref=e473]:
                        - /placeholder: Any other details about insurance handling, special arrangements, or internal reminders...
                        - text: WQQWQWWQWQQWWQQWWQWWQWWQQWQWWQWQQWWQQWWQWWQWWQQWQWWQWQQWWQQWWQWWQWWQQWQWWQWQQWWQQWWQWWQWWQQWQWWQWQQWWQQWWQWWQWWQQWQWWQWQQWWQQWWQWWQWWQQWQWWQWQQWWQQWWQWWQWWQQWQWWQWQQWWQQWWQWWQWWQQWQWWQWQQWWQQWWQWWQWWQQWQWWQWQQWWQQWWQWWQWWQQWQWWQWQQWWQQWWQWWQWWQQWQWWQWQQWWQQWWQWWQWWQQWQWWQWQQWWQQWWQWWQWWQQWQWWQWQQWWQQWWQWWQWWQQWQWWQWQQWWQQWWQWWQWWQQWQWWQWQQWWQQWWQWWQWWQQWQWWQWQQWWQQWWQWWQWWQQWQWWQWQQWWQQWWQWWQWWQQWQWWQWQQWWQQWWQWWQWWQQWQWWQWQQWWQQWWQWWQWWQQWQWWQWQQWWQQWWQWWQWWQQWQWWQWQQWWQQWWQWWQWWQQWQWWQWQQWWQQWWQWWQWWQQWQWWQWQQWWQQWWQWWQWWQQWQWWQWQQWWQQWWQWWQWWQQWQWWQWQQWWQQWWQWWQWWQQWQWWQWQQWWQQWWQWWQWWQQWQWWQWQQWWQQWWQWWQWWQQWQWWQWQQWWQQWWQWWQWWQQWQWWQWQQWWQQWWQWWQWWQQWQWWQWQQWWQQWWQWWQWWQQWQWWQWQQWWQQWWQWWQWWQQWQWWQWQQWWQQWWQWWQWWQQWQWWQWQQWWQQWWQWWQWWQQWQWWQWQQWWQQWWQWWQWWQQWQWWQWQQWWQQWWQWWQWWQQWQWWQWQQWWQQWWQWWQWWQQWQWWQWQQWWQQWWQWWQWWQQWQWWQWQQWWQQWWQWWQWWQQWQWWQWQQWWQQWWQWWQWWQQWQWWQWQQWWQQWWQWWQWWQQWQWWQWQQWWQQWWQWWQWWQQWQWWQWQQWWQQWWQWWQWWQQWQWWQWQQWWQQWWQWWQWWQQWQWWQWQQWWQQWWQWWQWWQQWQWWQWQQWWQQWWQWWQWWQQWQWWQWQQWWQQWWQWWQWWQQWQWWQWQQWWQQWWQWWQWWQQWQWWQWQQWWQQWWQWWQWWQQWQWWQWQQWWQQWWQWWQWWQQWQWWQWQQWWQQWWQWWQWWQQWQWWQWQQWWQQWWQWWQWWQQWQWWQWQQWWQQWWQWWQWWQQWQWWQWQQWWQQWWQWWQWWQQWQWWQWQQWWQQWWQWWQWWQQWQWWQWQQWWQQWWQWWQWWQQWQWWQWQQWWQQWWQWWQWWQQWQWWQWQQWWQQWWQWWQWWQQWQWWQWQQWWQQWWQWWQWWQQWQWWQWQQWWQQWWQWWQWWQQWQWWQWQQWWQQWWQWWQWWQQWQWWQWQQWWQQWWQWWQWWQQWQWWQWQQWWQQWWQWWQWWQQWQWWQWQQWWQQWWQWWQWWQQWQWWQWQQWWQQWWQWWQWWQQWQWWQWQQWWQQWWQWWQWWQQWQWWQWQQWWQQWWQWWQWWQQWQWWQWQQWWQQWWQWWQWWQQWQWWQWQQWWQQWWQWWQWWQQWQWWQWQQWWQQWWQWWQWWQQWQWWQWQQWWQQWWQWWQWWQQWQWWQWQQWWQQWWQWWQWWQQWQWWQWQQWWQQWWQWWQWWQQWQWWQWQQWWQQWWQWWQWWQQWQWWQWQQWWQQWWQWWQWWQQWQWWQWQQWWQQWWQWWQWWQQWQWWQWQQWWQQWWQWWQWWQQWQWWQWQQWWQQWWQWWQWWQQWQWWQWQQWWQQWWQWWQWWQQWQWWQWQQWWQQWWQWWQWWQQWQWWQWQQWWQQWWQWWQWWQQWQWWQWQQWWQQWWQWWQWWQQWQWWQWQQWWQQWWQWWQWWQQWQWWQWQQWWQQWWQWWQWWQQWQWWQWQQWWQQWWQWWQWWQQWQWWQWQQWWQQWWQWWQWWQQWQWWQWQQWWQQWWQWWQWWQQWQWWQWQQWWQQWWQWWQWWQQWQWWQWQQWWQQWWQWWQWWQQWQWWQWQQWWQQWWQWWQWWQQWQWWQWQQWWQQWWQWWQWWQQWQWWQWQQWWQQWWQWWQWWQQWQWWQWQQWWQQWWQWWQWWQQWQWWQWQQWWQQWWQWWQWWQQWQWWQWQQWWQQWWQWWQWWQQWQWWQWQQWWQQWWQWWQWWQQWQWWQWQQWWQQWWQWWQWWQQWQWWQWQQWWQQWWQWWQWWQQWQWWQWQQWWQQWWQWWQWWQQWQWWQWQQWWQQWWQWWQWWQQWQWWQWQQWWQQWWQWWQWWQQWQWWQWQQWWQQWWQWWQWWQQWQWWQWQQWWQQWWQWWQWWQQWQWWQWQQWWQQWWQWWQWWQQWQWWQWQQWWQQWWQWWQWWQQWQWWQWQQWWQQWWQWWQWWQQWQWWQWQQWWQQWWQWWQWWQQWQWWQWQQWWQQWWQWWQWWQQWQWWQWQQWWQQWWQWWQWWQQWQWWQWQQWWQQWWQWWQWWQQWQWWQWQQWWQQWWQWWQWWQQWQWWQWQQWWQQWWQWWQWWQQWQWWQWQQWWQQWWQWWQWWQQWQWWQWQQWWQQWWQWWQWWQQWQWWQWQQWWQQWWQWWQWWQQWQWWQWQQWWQQWWQWWQWWQQWQWWQWQQWWQQWWQWWQWWQQWQWWQWQQWWQQWWQWWQWWQQWQWWQWQQWWQQWWQWWQWWQQWQWWQWQQWWQQWWQWWQWWQQWQWWQWQQWWQQWWQWWQWWQQWQWWQWQQWWQQWWQWWQWWQQWQWWQWQQWWQQWWQWWQWWQQWQWWQWQQWWQQWWQWWQWWQQWQWWQWQQWWQQWWQWWQWWQQWQWWQWQQWWQQWWQWWQWWQQWQWWQWQQWWQQWWQWWQWWQQWQWWQWQQWWQQWWQWWQWWQQWQWWQWQQWWQQWWQWWQWWQQWQWWQWQQWWQQWWQWWQWWQQWQWWQWQQWWQQWWQWWQWWQQWQWWQWQQWWQQWWQWWQWWQQWQWWQWQQWWQQWWQWWQWWQQWQWWQWQQWWQQWWQWWQWWQQWQWWQWQQWWQQWWQWWQWWQQWQWWQWQQWWQQWWQWWQWWQQWQWWQWQQWWQQWWQWWQWWQQWQWWQWQQWWQQWWQWWQWWQQWQWWQWQQWWQQWWQWWQWWQQWQWWQWQQWWQQWWQWWQWWQQWQWWQWQQWWQQWWQWWQWWQQWQWWQWQQWWQQWWQWWQWWQQWQWWQWQQWWQQWWQWWQWWQQWQWWQWQQWWQQWWQWWQWWQQWQWWQWQQWWQQWWQWWQWWQQWQWWQWQQWWQQWWQWWQWWQQWQWWQWQQWWQQWWQWWQWWQQWQWWQWQQWWQQWWQWWQWWQQWQWWQWQQWWQQWWQWWQWWQQWQWWQWQQWWQQWWQWWQWWQQWQWWQWQQWWQQWWQWWQWWQQWQWWQWQQWWQQWWQWWQWWQQWQWWQWQQWWQQWWQWWQWWQQWQWWQWQQWWQQWWQWWQWWQQWQWWQWQQWWQQWWQWWQWWQQWQWWQWQQWWQQWWQWWQWWQQWQWWQWQQWWQQWWQWWQWWQQWQWWQWQQWWQQWWQWWQWWQQWQWWQWQQWWQQWWQWWQWWQQWQWWQWQQWWQQWWQWWQWWQQWQWWQWQQWWQQWWQWWQWWQQWQWWQWQQWWQQWWQWWQWWQQWQWWQWQQWWQQWWQWWQWWQQWQWWQWQQWWQQWWQWWQWWQQWQWWQWQQWWQQWWQWWQWWQQWQWWQWQQWWQQWWQWWQWWQQWQWWQWQQWWQQWWQWWQWWQQWQWWQWQQWWQQWWQWWQWWQQWQWWQWQQWWQQWWQWWQWWQQWQWWQWQQWWQQWWQWWQWWQQWQWWQWQQWWQQWWQWWQWWQQWQWWQWQQWWQQWWQWWQWWQQWQWWQWQQWWQQWWQWWQWWQQWQWWQWQQWWQQWWQWWQWWQQWQWWQWQQWWQQWWQWWQWWQQWQWWQWQQWWQQWWQWWQWWQQWQWWQWQQWWQQWWQWWQWWQQWQWWQWQQWWQQWWQWWQWWQQWQWWQWQQWWQQWWQWWQWWQQWQWWQWQQWWQQWWQWWQWWQQWQWWQWQQWWQQWWQWWQWWQQWQWWQWQQWWQQWWQWWQWWQQWQWWQWQQWWQQWWQWWQWWQQWQWWQWQQWWQQWWQWWQWWQQWQWWQWQQWWQQWWQWWQWWQQWQWWQWQQWWQQWWQWWQWWQQWQWWQWQQWWQQWWQWWQWWQQWQWWQWQQWWQQWWQWWQWWQQWQWWQWQQWWQQWWQWWQWWQQWQWWQWQQWWQQWWQWWQWWQQWQWWQWQQWWQQWWQWWQWWQQWQWWQWQQWWQQWWQWWQWWQQWQWWQWQQWWQQWWQWWQWWQQWQWWQWQQWWQQWWQWWQWWQQWQWWQWQQWWQQWWQWWQWWQQWQWWQWQQWWQQWWQWWQWWQQWQWWQWQQWWQQWWQWWQWWQQWQWWQWQQWWQQWWQWWQWWQQWQWWQWQQWWQQWWQWWQWWQQWQWWQWQQWWQQWWQWWQWWQQWQWWQWQQWWQQWWQWWQWWQQWQWWQWQQWWQQWWQWWQWWQQWQWWQWQQWWQQWWQWWQWWQQWQWWQWQQWWQQWWQWWQWWQQWQWWQWQQWWQQWWQWWQWWQQWQWWQWQQWWQQWWQWWQWWQQWQWWQWQQWWQQWWQWWQWWQQWQWWQWQQWWQQWWQWWQWWQQWQWWQWQQWWQQWWQWWQWWQQWQWWQWQQWWQQWWQWWQWWQQWQWWQWQQWWQQWWQWWQWWQQWQWWQWQQWWQQWWQWWQWWQQWQWWQWQQWWQQWWQWWQWWQQWQWWQWQQWWQQWWQWWQWWQQWQWWQWQQWWQQWWQWWQWWQQWQWWQWQQWWQQWWQWWQWWQQWQWWQWQQWWQQWWQWWQWWQQWQWWQWQQWWQQWWQWWQWWQQWQWWQWQQWWQQWWQWWQWWQQWQWWQWQQWWQQWWQWWQWWQQWQWWQWQQWWQQWWQWWQWWQQWQWWQWQQWWQQWWQWWQWWQQWQWWQWQQWWQQWWQWWQWWQQWQWWQWQQWWQQWWQWWQWWQQWQWWQWQQWWQQWWQWWQWWQQWQWWQWQQWWQQWWQWWQWWQQWQWWQWQQWWQQWWQWWQWWQQWQW
                      - paragraph [ref=e474]: Extra insurance information that the AI should know about
                      - paragraph [ref=e475]: 5000/500
                - generic [ref=e476]:
                  - button "Cancel" [ref=e477] [cursor=pointer]
                  - button "Save Changes" [disabled] [ref=e478]
```

# Test source

```ts
  1   | import { test, expect } from '../../src/fixtures';
  2   | import { InsuranceBillingPage } from '../../src/pages/InsuranceBillingPage';
  3   | import { BasePage } from '../../src/pages/BasePage';
  4   | 
  5   | /**
  6   |  * Coverage — Accepted Insurance Plans
  7   |  * IB-COV-R1 to R10
  8   |  */
  9   | 
  10  | test.describe('Coverage — Accepted Insurance Plans', () => {
  11  |   test.beforeEach(async ({ insuranceBilling }) => {
  12  |     await insuranceBilling.openEdit(InsuranceBillingPage.CARD.coverage);
  13  |   });
  14  | 
  15  |   test.afterEach(async ({ insuranceBilling }) => {
  16  |     await insuranceBilling.cancel();
  17  |   });
  18  | 
  19  |   // -------------------------------------------------------------------------
  20  |   // Smoke
  21  |   // -------------------------------------------------------------------------
  22  | 
  23  |   test('panel opens with required elements', async ({ insuranceBilling }) => {
  24  |     await expect(insuranceBilling.modal).toBeVisible();
  25  |     await expect(insuranceBilling.cancelButton).toBeVisible();
  26  |     await expect(insuranceBilling.addCustomButton).toBeVisible();
  27  |   });
  28  | 
  29  |   test('Add Custom reveals New Plan form', async ({ insuranceBilling }) => {
  30  |     await insuranceBilling.addCustomButton.click();
  31  |     await insuranceBilling.page.waitForTimeout(500);
  32  |     await expect(insuranceBilling.insuranceNameInput).toBeVisible();
  33  |     await expect(insuranceBilling.payerIdInput).toBeVisible();
  34  |   });
  35  | 
  36  |   // -------------------------------------------------------------------------
  37  |   // IB-COV-R1 — Accept All Toggle
  38  |   // -------------------------------------------------------------------------
  39  | 
  40  |   test('Accept All toggle changes state and saves', async ({ insuranceBilling }) => {
  41  |     const toggle = insuranceBilling.acceptAllToggle;
  42  |     const initial = await toggle.getAttribute('aria-checked');
  43  |     await toggle.click();
  44  |     await insuranceBilling.page.waitForTimeout(800);
  45  |     const after = await toggle.getAttribute('aria-checked');
  46  |     expect(after).not.toBe(initial);
  47  |     await insuranceBilling.saveAndAssertSuccess();
  48  |   });
  49  | 
  50  |   // -------------------------------------------------------------------------
  51  |   // IB-COV-R2 — Insurance Name
  52  |   // -------------------------------------------------------------------------
  53  | 
  54  |   test('valid plan saves via Add Custom flow', async ({ insuranceBilling }) => {
  55  |     await insuranceBilling.addPlan({
  56  |       name: BasePage.unique('Delta'),
  57  |       payerId: '99001',
  58  |     });
  59  |   });
  60  | 
  61  |   test('empty name → Save Plan disabled or error', async ({ insuranceBilling }) => {
  62  |     await insuranceBilling.addCustomButton.click();
  63  |     await insuranceBilling.page.waitForTimeout(500);
  64  |     await insuranceBilling.insuranceNameInput.press('Tab');
  65  |     await insuranceBilling.page.waitForTimeout(500);
  66  | 
  67  |     const isDisabled = await insuranceBilling.savePlanButton.isDisabled();
  68  |     const hasError = await insuranceBilling.error.isVisible();
  69  |     expect(isDisabled || hasError).toBeTruthy();
  70  |   });
  71  | 
  72  |   test('1-char name → at least 2 characters error', async ({ insuranceBilling }) => {
  73  |     await insuranceBilling.addCustomButton.click();
  74  |     await insuranceBilling.page.waitForTimeout(500);
> 75  |     await insuranceBilling.smartFill(insuranceBilling.insuranceNameInput, 'D');
      |                            ^ TypeError: insuranceBilling.smartFill is not a function
  76  |     await insuranceBilling.insuranceNameInput.press('Tab');
  77  |     await insuranceBilling.page.waitForTimeout(500);
  78  |     await expect(insuranceBilling.error).toContainText('at least 2 characters');
  79  |   });
  80  | 
  81  |   test('2-char name — minimum valid', async ({ insuranceBilling }) => {
  82  |     await insuranceBilling.addCustomButton.click();
  83  |     await insuranceBilling.page.waitForTimeout(500);
  84  |     await insuranceBilling.smartFill(insuranceBilling.insuranceNameInput, 'AB');
  85  |     await insuranceBilling.insuranceNameInput.press('Tab');
  86  |     await insuranceBilling.page.waitForTimeout(500);
  87  |     const nameError = insuranceBilling.modal
  88  |       .locator("p[id$='-error']")
  89  |       .filter({ hasText: 'characters' });
  90  |     await expect(nameError).not.toBeVisible();
  91  |   });
  92  | 
  93  |   test('XSS in name → blocked', async ({ insuranceBilling }) => {
  94  |     await insuranceBilling.addCustomButton.click();
  95  |     await insuranceBilling.page.waitForTimeout(500);
  96  |     await insuranceBilling.smartFill(
  97  |       insuranceBilling.insuranceNameInput,
  98  |       '<script>alert(1)</script>'
  99  |     );
  100 |     await insuranceBilling.insuranceNameInput.press('Tab');
  101 |     await insuranceBilling.page.waitForTimeout(500);
  102 |     const isDisabled = await insuranceBilling.savePlanButton.isDisabled();
  103 |     const hasError = await insuranceBilling.error.isVisible();
  104 |     expect(isDisabled || hasError).toBeTruthy();
  105 |   });
  106 | 
  107 |   test('error clears when name corrected', async ({ insuranceBilling }) => {
  108 |     await insuranceBilling.addCustomButton.click();
  109 |     await insuranceBilling.page.waitForTimeout(500);
  110 |     await insuranceBilling.smartFill(insuranceBilling.insuranceNameInput, 'D');
  111 |     await insuranceBilling.insuranceNameInput.press('Tab');
  112 |     await insuranceBilling.page.waitForTimeout(500);
  113 |     await expect(insuranceBilling.error).toBeVisible();
  114 | 
  115 |     await insuranceBilling.smartFill(insuranceBilling.insuranceNameInput, 'Delta Dental');
  116 |     await insuranceBilling.insuranceNameInput.press('Tab');
  117 |     await insuranceBilling.page.waitForTimeout(500);
  118 |     await expect(insuranceBilling.error).not.toBeVisible();
  119 |   });
  120 | 
  121 |   // -------------------------------------------------------------------------
  122 |   // IB-COV-R8 — Coverage %
  123 |   // -------------------------------------------------------------------------
  124 | 
  125 |   test('coverage % > 100 → blocked', async ({ insuranceBilling }) => {
  126 |     await insuranceBilling.addCustomButton.click();
  127 |     await insuranceBilling.page.waitForTimeout(500);
  128 |     await insuranceBilling.fillCoveragePercentage(insuranceBilling.preventiveInput, '101');
  129 |     const isDisabled = await insuranceBilling.savePlanButton.isDisabled();
  130 |     const errors = await insuranceBilling.modal.locator("p[id$='-error']").count();
  131 |     expect(isDisabled || errors > 0).toBeTruthy();
  132 |   });
  133 | 
  134 |   test('coverage % = 0 → minimum valid', async ({ insuranceBilling }) => {
  135 |     await insuranceBilling.addCustomButton.click();
  136 |     await insuranceBilling.page.waitForTimeout(500);
  137 |     await insuranceBilling.fillCoveragePercentage(insuranceBilling.preventiveInput, '0');
  138 |     const pctError = insuranceBilling.modal
  139 |       .locator("p[id$='-error']")
  140 |       .filter({ hasText: 'Preventive' });
  141 |     await expect(pctError).not.toBeVisible();
  142 |   });
  143 | 
  144 |   test('coverage % = 100 → maximum valid', async ({ insuranceBilling }) => {
  145 |     await insuranceBilling.addCustomButton.click();
  146 |     await insuranceBilling.page.waitForTimeout(500);
  147 |     await insuranceBilling.fillCoveragePercentage(insuranceBilling.preventiveInput, '100');
  148 |     const pctError = insuranceBilling.modal
  149 |       .locator("p[id$='-error']")
  150 |       .filter({ hasText: 'Preventive' });
  151 |     await expect(pctError).not.toBeVisible();
  152 |   });
  153 | 
  154 |   test('plan with coverage % saves', async ({ insuranceBilling }) => {
  155 |     await insuranceBilling.addPlan({
  156 |       name: BasePage.unique('Coverage'),
  157 |       payerId: '55555',
  158 |       preventive: '75',
  159 |       basic: '80',
  160 |     });
  161 |   });
  162 | 
  163 |   // -------------------------------------------------------------------------
  164 |   // IB-COV-R10 — Additional Notes
  165 |   // -------------------------------------------------------------------------
  166 | 
  167 |   test('additional notes 500 chars accepted', async ({ insuranceBilling }) => {
  168 |     await insuranceBilling.smartFill(insuranceBilling.additionalNotes, 'A'.repeat(500));
  169 |     await insuranceBilling.page.waitForTimeout(500);
  170 |     const errors = await insuranceBilling.modal.locator("p[id$='-error']").count();
  171 |     expect(errors).toBe(0);
  172 |   });
  173 | 
  174 |   test('additional notes > 500 chars blocked', async ({ insuranceBilling }) => {
  175 |     await insuranceBilling.smartFill(insuranceBilling.additionalNotes, 'A'.repeat(501));
```