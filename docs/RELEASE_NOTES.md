Imported recipes now get structured ingredients.

- After the import, the ingredients are run through Mealie's ingredient parser (AI when OpenAI is configured in Mealie, otherwise the built-in parser) and linked to your existing foods and units.
- Lines whose food is not in Mealie stay as text, so no duplicate foods are created; an unknown unit is kept in the note.
- The panel shows how many ingredients were linked.
