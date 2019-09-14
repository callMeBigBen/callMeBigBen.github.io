# OpenStack设计与实现阅读笔记

- OpenStack是AWS的小弟
- 与运行在物理节点上的hypervisor进行交互，实现对硬件资源的管理和控制
- Nova - ec2
- swift - s3
- cinder - ebs
- keystone - iam

## Nova

- provide VM service. The overall controller. Compatible to EC2 api as well.
- Nova components:
  1. Nova-api: