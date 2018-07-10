#!/usr/bin/env bats

@test "valid iso generated" {
   file test/cloudinit.iso | grep "ISO 9660 CD-ROM"
}