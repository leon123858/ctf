# magic

pwn 題

## 題目

https://bamboofox.cs.nctu.edu.tw/courses/1/challenges/1

Description
`nc bamboofox.cs.nctu.edu.tw 10000`

Do you believe in magic?

Hint
Stack buffer overflow

```
void do_magic(char *buf,int n)
{
        int i;
        srand(time(NULL));
        for (i = 0; i < n; i++)
                buf[i] ^= rand()%256;
}

void magic()
{
        char magic_str[60];
        scanf("%s", magic_str);
        do_magic(magic_str, strlen(magic_str));
        printf("%s", magic_str);
}
```
