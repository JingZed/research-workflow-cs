# Candidate Board

- figure_id: <id>
- source_spec: <path>
- requested_scope: <one direction | two directions | explicit broad exploration>
- reference: <path and role, or none>

| id | file | source | layout | five-second payoff | main risk |
| --- | --- | --- | --- | --- | --- |
| A | <path> | <imagegen/provided> | <short> | <short> | <short> |
| B | <path or omitted> | <imagegen/provided> | <short> | <short> | <short> |

## Selection

- selected: <A | B | none>
- selected_path: <path or none>
- reason: <one short paragraph>
- traits_to_preserve: <3-5 visible traits, or none>

If no candidate is suitable, record `selected: none` and stop. Do not add
routing, retry, gate, reviewer, or next-owner fields.
