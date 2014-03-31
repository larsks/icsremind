This is a simple script for generating [remind][] calendars from a
CalDAV server.


Synopsis
========

    icsremind [-h] [--config CONFIG] [--days DAYS] [--output OUTPUT]

Configuration
=============

ICSRemind reads configuration from a [YAML][] format configuration
file.  By default it will look for
`~/.config/icsremind/icsremind.yaml`, but you can specify an
alternative using the `--config` command line option or by setting the
`ICSREMIND_CONFIG` environment variable.

The configuration looks something like this:

    icsremind:
      url: https://mail.corp.example.com/dav/myname@example.com/
      username: myname
      password: supersecret
      calendars:
        "https://mail.corp.example.com/dav/myname@example.com/Calendar":
          priority: 9000
        "https://mail.corp.example.com/dav/mynameg@example.com/Tasks":
          priority: 9000
        "https://mail.corp.example.com/dav/mynameg@example.com/Company%20Calendar's%20Calendar":

Hopefully `url`, `username`, and `password` are self explanatory.

The `calendars` section is optional.  If specified, ICSRemind will only process calendars with URLs that are explicitly listed in this section.  For each listed calendar, you may specify a set of options.  Currently supported options are:

- `priority <nnnn>` -- set a priority for `remind` entries generated
  from this calendar.

[remind]: http://www.roaringpenguin.com/products/remind

