import { readFileSync } from "fs";
import Ajv from "ajv";

const ajv = new Ajv({ allErrors: true });

const schema = JSON.parse(
  readFileSync("schemas/repo-metadata.schema.json", "utf8")
);
const validate = ajv.compile(schema);

const inventory = JSON.parse(
  readFileSync("inventory/repos.json", "utf8")
);

let hasErrors = false;

for (const repo of inventory.repos) {
  const valid = validate(repo);
  if (!valid) {
    hasErrors = true;
    console.error(`Validation errors for ${repo.full_name}:`);
    console.error(validate.errors);
  }
}

if (hasErrors) {
  console.error("Validation failed.");
  process.exit(1);
} else {
  console.log("All repos passed schema validation.");
}
