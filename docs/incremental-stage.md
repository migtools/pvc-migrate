# Incremental staging

**Stage 3** of `pvc-migrate` is responsible of running the rsync transfers for the PVCs discovered. An incremental **stage 3** might be desired to reduce the amount of data and time required during the final migration.

## Overview

There are three basic steps during an incremental staged migration :

1. An incremental stage assumes you have finished the **initial** data sync by completing [Stage 1](../1_pvc_data_gen), [Stage2](../2_pvc_destination_gen) and [Stage3](../3_run_rsync) for the desired namespace(s)
2. Perform incremental stage 3 rsync as many times as necessary
3. Perform final stage 3 rsync with applications quiesced

### Considerations

- Rsync will re-transfer updated data on each stage 3 incremental pass, the closer to the final migration you can stage data the greater the benefits. This specially applies to applications that exhibit a high data rate change
- When dealing with large files, consider using --inplace and --whole-file rsync options, see large files notes below.

### Rsync flags tuning

The ansible variable that controls rsync flags is __rsync_opts__ , below is an example run of stage 3 altering default rsync flags

```
ansible-playbook run-rsync.yml -e "rsync_opts='-aPvvHh --delete --inplace'"
```

Note: The default rsync flags are stored [here](../3_run_rsync/defaults.yml)

### Enable ansible profile_tasks

The ansible profile_tasks callback enables timers for all tasks being run, useful for timing the rsync transfers on stage 3. You can whitelist it on ansible.cfg by adding: 
```
[defaults]
callback_whitelist = profile_tasks

[callback_profile_tasks]
task_output_limit = 40
```

### Large files

Rsync defaults might not be ideal for large file workloads (i.e databases), these flags could help on these cases:

- Block-level replication (--inplace) : Rsync will write updated data directly to a file, instead of making a copy and moving it into place. This can reduce significantly the amount of data written to the destination PVCs since there is no temporary file being created. **Please use with care and read warnings on rsync man page**

- Whole file (--whole-file) : It will disable rsync delta-transfer algorithm and transfer the entire file if size or modification time has changed, if source and destination are connected via a high speed network faster than the I/O bandwidth to disk (specially for slow network filesystems), this can significantly reduce overhead and speed up the sync.

It is suggested to make a few test runs with your large file workload to get an idea what is optimal or more suitable for your environment.
