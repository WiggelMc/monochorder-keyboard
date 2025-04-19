export type DeepPartial<T, Blacklist = never> = T extends Blacklist
    ? T
    : { [K in keyof T]?: DeepPartial<T[K], Blacklist> }