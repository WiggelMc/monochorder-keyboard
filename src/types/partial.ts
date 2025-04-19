export type DeepPartial<T, Blacklist = never> =
    ([T] extends [Blacklist]
        ? T
        : (T extends (infer A)[]
            ? (DeepPartial<A, Blacklist>)[]
            : (T extends object
                ? { [K in keyof T]?: DeepPartial<T[K], Blacklist> }
                : T
            )
        )
    )
