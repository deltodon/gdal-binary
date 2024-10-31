# Documentation



### Makefile

Here's a shell command that will return the Docker container ID for a container with a name starting with "cibuildwheel-":

```bash
docker ps --format '{{.ID}}\t{{.Names}}' | awk '/cibuildwheel-/ {print $1}'
```

This command does the following:

1. `docker ps` lists all running containers.
2. The `--format` option specifies that we only want the container ID and name.
3. The output is piped to `awk`.
4. `awk` searches for lines containing "cibuildwheel-" and prints the first field (the container ID).

This command will return the container ID (e.g., "74f675254847") for any running container whose name starts with "cibuildwheel-".

If you want to include stopped containers as well, you can add the `-a` flag to the `docker ps` command:

```bash
docker ps -a --format '{{.ID}}\t{{.Names}}' | awk '/cibuildwheel-/ {print $1}'
```

This will return the container ID for any container (running or stopped) whose name starts with "cibuildwheel-".

Certainly! I'll update the Makefile with the command we just created. Here's the updated version:

```makefile
attach:
	@docker start -ai $$(docker ps -a --format '{{.ID}}\t{{.Names}}' | awk '/cibuildwheel-/ {print $$1}')
```

Here's an explanation of the changes:

1. We've replaced `$(CONT)` with the command to find the container ID.
2. We've wrapped the entire command in `$$(...)` to ensure it's evaluated in the shell when the make target is run.
3. We've used `docker ps -a` to include stopped containers, as the `docker start` command can work on stopped containers.
4. We've escaped the `$` in `$$1` in the awk command, as make uses `$` for its own variable substitution.

This solution should work as follows:

1. It will find the container ID of a container whose name starts with "cibuildwheel-", whether it's running or stopped.
2. If found, it will start the container (if it's not already running) and attach to it interactively.

Note that if there are multiple containers with names starting with "cibuildwheel-", this will attach to the first one found. If you need to handle multiple containers, you might need to adjust the logic further.

Also, make sure there's a tab at the beginning of the second line, not spaces, as Makefiles require tabs for indentation.