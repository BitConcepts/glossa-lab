-- Spec 083 Step 3 (T026): workspaces gain the description line the
-- admin screen's create form collects and the workspace cards show
-- (wireframe 09: "the question or scope this workspace holds").
-- Nullable: workspaces created before this migration simply have no
-- description, and the surfaces render the name alone.
ALTER TABLE workspaces ADD COLUMN description TEXT;
