#ifndef __RFS_H__
#define __RFS_H__

extern void *rfs_open(void *base_addr, int size);
extern void rfs_close(void *handle);

extern int rfs_seek(void *handle, int offset);
extern int rfs_read(void *handle, void *buffer, int length);

#endif
