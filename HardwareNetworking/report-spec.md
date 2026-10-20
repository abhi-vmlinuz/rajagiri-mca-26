# Project Report Specification: RCSS Campus Network

## Objective

Generate a formal academic PDF project report titled **“Design and Implementation of the RCSS Campus Network Using Cisco Packet Tracer.”**

The report must document the network topology, subnetting calculations, VLAN design, IP addressing, Cisco IOS configuration, DHCP, verification results, and limitations. Use the actual Packet Tracer project and genuine screenshots as the source of evidence.

### Input files

- Existing Packet Tracer project: use the actual `.pkt` filename in the project directory.
- Screenshots: `screenshots/`
- This specification: `REPORT_SPEC.md`

### Output files

- `report.md` — editable Markdown report.
- `report.pdf` — compiled PDF report.

Do not modify the original `.pkt` file or network configuration while generating the report.

## 1. Cover page

Include:

- Project title.
- Course or subject name.
- Student name and register/roll number.
- Institution name, if confirmed.
- Faculty or lecturer name.
- Academic year and submission date.

Use clearly marked placeholders for information not supplied. Never invent student details, course information, or submission details.

## 2. Abstract

Write one concise paragraph describing the simulated campus network and its implementation using four VLANs, IEEE 802.1Q trunking, router-on-a-stick, DHCP pools, static server addressing, and connectivity tests.

Only claim features that were actually configured and verified.

## 3. Objectives

List the project objectives:

1. Design a multi-building campus network topology.
2. Segment endpoints using VLANs.
3. Configure switch access ports and trunk links.
4. Configure inter-VLAN routing using router-on-a-stick.
5. Provide dynamic IPv4 addressing through DHCP.
6. Assign a static IP address to the server.
7. Test gateway and inter-VLAN connectivity.
8. Save and document the network configuration.

## 4. Tools and technologies

Document the technologies actually used:

- Cisco Packet Tracer.
- Cisco 2911 router.
- Cisco 2960 switches.
- Ethernet cabling.
- IPv4 subnetting.
- VLANs.
- IEEE 802.1Q.
- DHCP.
- ICMP ping.

## 5. Requirements and assumptions

Explain the need to connect three buildings, separate traffic into logical VLANs, provide default gateways, automatically assign client addresses, and make the server reachable.

State that this is a simulated network. Do not claim that ACLs, firewall policies, DNS, Internet connectivity, redundancy, authentication, or production security were implemented unless there is actual evidence.

## 6. Physical topology

Insert `screenshots/01_full_topology.png` as Figure 1.

Describe the router-to-core connection, the three building uplinks, and endpoint connections. Explain that VLAN membership depends on switch-port configuration rather than physical building location.

Include this uplink table:

| Device A | Port A | Device B | Port B | Purpose |
|---|---|---|---|---|
| RCSS-R1 | Gi0/0 | RCSS-SW-CORE | Gi0/1 | Router-on-a-stick trunk |
| RCSS-SW-CORE | Gi0/2 | RCSS-SW-ASSUMPTION | Gi0/1 | Building uplink |
| RCSS-SW-CORE | Fa0/1 | RCSS-SW-CARMEL | Gi0/1 | Building uplink |
| RCSS-SW-CORE | Fa0/2 | RCSS-SW-OLDBLOCK | Gi0/1 | Building uplink |

Mention that the Carmel and Old Block uplinks use Fast Ethernet ports on the core switch, so their physical link speed is limited by those interfaces.

## 7. Logical design and VLAN plan

Include this table:

| VLAN ID | Name on core | Purpose | Subnet | Gateway |
|---|---|---|---|---|
| 10 | ASSUMPTION-BLOCK | Assumption and selected shared devices | 192.168.10.0/24 | 192.168.10.1 |
| 20 | CARMEL-BLOCK | Carmel Faculty | 192.168.20.0/24 | 192.168.20.1 |
| 30 | OLDBLOCK_LAB | Old Block lab and reception | 192.168.30.0/24 | 192.168.30.1 |
| 40 | SERVERS | Server network | 192.168.40.0/24 | 192.168.40.1 |

Document these endpoint assignments:

- Assumption Admin01, Admin02, and Faculty01: VLAN 10.
- RCSS-SRV01: VLAN 40.
- RCSS-PRT-01, RCSS-RECEPTION, and RCSS-OFFICE: VLAN 10.
- CARMEL-FACULTY01: VLAN 20.
- RCSS-LAB01, RCSS-LAB02, and RCSS-OLD-RECEPTION: VLAN 30.

Explain that VLAN names can differ between switches. For example, VLAN 30 may be named `OLDBLOCK_LAB` on the core and `OLDBLOCK-LAB` on Old Block. The numeric VLAN ID is what must match for traffic to be classified into the same VLAN across trunks.

Insert Figures 2–7 as appropriate to document router interfaces, VLAN membership, and trunk status.

## 8. Subnetting calculations

Show the mathematical derivation.

Each subnet uses mask `255.255.255.0`, which is `/24`.

- IPv4 address length: 32 bits.
- Network bits: 24.
- Host bits: `32 - 24 = 8`.
- Total addresses: `2^8 = 256`.
- Conventional usable host addresses: `256 - 2 = 254`.

Explain that the network address and broadcast address are not assigned to ordinary hosts.

Include this table:

| VLAN | Network address | First usable | Last usable | Broadcast |
|---|---|---|---|---|
| 10 | 192.168.10.0/24 | 192.168.10.1 | 192.168.10.254 | 192.168.10.255 |
| 20 | 192.168.20.0/24 | 192.168.20.1 | 192.168.20.254 | 192.168.20.255 |
| 30 | 192.168.30.0/24 | 192.168.30.1 | 192.168.30.254 | 192.168.30.255 |
| 40 | 192.168.40.0/24 | 192.168.40.1 | 192.168.40.254 | 192.168.40.255 |

Explain that `.0` is the network address, `.255` is the broadcast address for these `/24` subnets, and `.1` is the router gateway.

## 9. IP addressing and DHCP plan

Include this table:

| VLAN | Subnet | Gateway | Excluded range | Expected available DHCP range |
|---|---|---|---|---|
| 10 | 192.168.10.0/24 | 192.168.10.1 | 192.168.10.1–192.168.10.20 | 192.168.10.21–192.168.10.254 |
| 20 | 192.168.20.0/24 | 192.168.20.1 | 192.168.20.1–192.168.20.20 | 192.168.20.21–192.168.20.254 |
| 30 | 192.168.30.0/24 | 192.168.30.1 | 192.168.30.1–192.168.30.20 | 192.168.30.21–192.168.30.254 |
| 40 | 192.168.40.0/24 | 192.168.40.1 | 192.168.40.1–192.168.40.20 | 192.168.40.21–192.168.40.254 |

Clarify that these are available ranges after exclusions; actual leases depend on client requests and addresses already in use.

Document the server configuration:

- IP address: `192.168.40.2`
- Subnet mask: `255.255.255.0`
- Default gateway: `192.168.40.1`
- DNS: blank unless a DNS service is actually configured.

The server's static address is excluded from DHCP allocation and should not appear as a DHCP lease.

Insert the DHCP and endpoint configuration screenshots.

## 10. Configuration procedure

Explain the implementation in this order:

1. Create VLANs on the core switch.
2. Configure the router-facing and building-facing core ports as trunks.
3. Create the relevant VLANs on each building switch.
4. Configure each building switch's uplink as a trunk.
5. Assign endpoint ports to the correct access VLAN.
6. Configure the router's physical interface and four 802.1Q subinterfaces.
7. Configure DHCP exclusions and four DHCP pools.
8. Configure the server with its static IPv4 address.
9. Set client PCs and printer to DHCP.
10. Verify VLANs, trunks, interfaces, DHCP leases, routes, and connectivity.

Include concise command examples, but use the actual configuration as the source of truth. Put lengthy configuration excerpts in an appendix rather than overwhelming the main body.

The router configuration should resemble:

```text
interface GigabitEthernet0/0
 no ip address
 no shutdown
!
interface GigabitEthernet0/0.10
 encapsulation dot1Q 10
 ip address 192.168.10.1 255.255.255.0
!
interface GigabitEthernet0/0.20
 encapsulation dot1Q 20
 ip address 192.168.20.1 255.255.255.0
!
interface GigabitEthernet0/0.30
 encapsulation dot1Q 30
 ip address 192.168.30.1 255.255.255.0
!
interface GigabitEthernet0/0.40
 encapsulation dot1Q 40
 ip address 192.168.40.1 255.255.255.0
```

If the actual configuration differs, document the observed configuration and flag discrepancies. Do not silently assume that a planned configuration was applied correctly.

## 11. Verification and results

Insert the relevant screenshots for:

- Router subinterface status.
- Core VLANs and trunk links.
- Building switch access-port membership.
- DHCP pools and leases.
- Endpoint IP configuration.
- Routing table.
- Gateway and inter-VLAN pings.

Include this test table and fill in the observed packet counts:

| Test | Source | Destination | Result |
|---|---|---|---|
| Gateway test | ASSUMPTION-ADMIN01 | 192.168.10.1 | Record observed result |
| Gateway test | RCSS-SRV01 | 192.168.40.1 | Record observed result |
| Inter-VLAN test | RCSS-SRV01 | Admin01's actual IP | Record observed result |
| Cross-building test | ASSUMPTION-ADMIN01 | Carmel Faculty01's actual IP | Record observed result |
| Inter-VLAN test | RCSS-LAB01 | 192.168.40.2 | Record observed result |

Use the exact packet counts in the screenshots. If two packets were sent and two replies were received, report `2 sent, 2 received, 0% loss`. Do not claim four packets if the screenshot shows only two.

Explain that a gateway ping proves reachability to the router interface. An endpoint-to-endpoint ping between different VLANs demonstrates inter-VLAN communication.

Do not claim that every endpoint was tested unless the evidence shows that.

## 12. Discussion

Explain:

- VLANs provide logical Layer 2 segmentation.
- Devices in different IP subnets use a default gateway to communicate.
- IEEE 802.1Q tags identify VLANs over trunk links.
- Router subinterfaces provide a gateway for each VLAN.
- DHCP exclusions protect gateway and reserved addresses.
- Successful pings demonstrate the specific paths tested, not every possible path.

Do not claim the network is secure or production-ready simply because pings succeed. The base design has no ACLs, so inter-VLAN routing is permitted by default.

## 13. Limitations and future improvements

Document the actual limitations, such as:

- Packet Tracer simulation rather than a live production deployment.
- No ACL-based inter-VLAN filtering.
- No DNS service unless configured.
- No WAN/Internet connection unless configured.
- No redundant router or switch links.
- No management VLAN or SSH management unless implemented.

Discuss ACLs, DNS, redundancy, port security, monitoring, and a management VLAN as possible future improvements. Label them as recommendations, not completed features.

## 14. Conclusion

Summarize the four VLANs, trunk links, router-on-a-stick configuration, DHCP pools, static server address, and verified connectivity tests. Only claim results supported by the actual screenshots.

## 15. Appendices

Include:

- Appendix A: Selected router configuration.
- Appendix B: Selected switch VLAN and trunk configuration.
- Appendix C: Additional DHCP and connectivity output.
- Appendix D: Device and port map, if useful.

Avoid duplicating screenshots already presented clearly in the main report.

## Figure and screenshot requirements

Use local relative paths, for example `screenshots/01_full_topology.png`.

Every figure must have:
- A sequential figure number.
- A descriptive caption.
- A sentence in the report explaining what it demonstrates.

Preserve image aspect ratios. Keep terminal text readable. Use landscape pages for wide images if necessary.

Do not create fake screenshots, fake CLI output, or placeholder images that appear to be real evidence. If a required screenshot is missing, list the missing filename and ask the student to capture it.

## PDF generation and quality checks

1. Produce `report.md` and `report.pdf`.
2. Use a formal academic layout with a cover page, table of contents, numbered headings, page numbers, tables, code blocks, and figure captions.
3. Use a Times New Roman-style font if installed. Before choosing a LaTeX font package, verify that its dependencies are available locally. If the preferred font package is unavailable, use a compatible installed font instead of leaving compilation broken.
4. Compile enough times to resolve the table of contents and cross-references.
5. Verify the PDF exists, is non-empty, and includes all intended figures.
6. Inspect rendered pages for clipped tables, unreadable terminal screenshots, blank pages, broken links, and overflow.
7. Keep the original Packet Tracer file unchanged.
8. Report any discrepancy between the screenshots and the planned configuration instead of concealing it.

### Final deliverables

- `report.md`
- `report.pdf`
- `screenshots/` containing the original evidence images
- The original Packet Tracer project preserved unchanged

