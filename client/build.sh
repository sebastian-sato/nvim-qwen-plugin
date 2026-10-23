gcc -shared -fPIC libqwenclient.c -o libqwenclient.so \
    -lcurl \
    $(pkg-config --cflags --libs lua5.4)
