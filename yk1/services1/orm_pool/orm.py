from orm_pool.mysql_pool import Mysql


class Field(object):
    def __init__(self, name, column_type, primary_key, default):
        self.name = name
        self.column_type = column_type
        self.primary_key = primary_key
        self.default = default


class IntegerField(Field):
    def __init__(self, name, column_type="int", primary_key=None, default=None):
        super().__init__(name, column_type, primary_key, default)


class StringField(Field):
    def __init__(self, name, column_type="varchar(255)", primary_key=None, default=None):
        super().__init__(name, column_type, primary_key, default)


class MyMetaClass(type):
    def __new__(cls, class_name, class_bases, class_attrs):
        if class_name == "Models":
            return super().__new__(cls, class_name, class_bases, class_attrs)

        table_name = class_attrs.get("table_name", class_name)
        primary_key = None
        mappings = {}

        for k, v in class_attrs.items():
            if isinstance(v, Field):
                mappings[k] = v
                if v.primary_key:
                    if primary_key:
                        raise TypeError("只能有一个主键！")
                    primary_key = k

        if not primary_key:
            raise TypeError("必须有一个主键！")

        for k in mappings:
            class_attrs.pop(k)

        class_attrs["table_name"] = table_name
        class_attrs["primary_key"] = primary_key
        class_attrs["mappings"] = mappings

        return super().__new__(cls, class_name, class_bases, class_attrs)


class Models(dict, metaclass=MyMetaClass):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def __getattr__(self, item):
        return self.get(item,"没有该键！")

    def __setattr__(self, key, value):
        self[key] = value

    @classmethod
    def select(cls,**kwargs):
        ms = Mysql()
        if not kwargs:
            sql = "select * from %s"%cls.table_name
            res = ms.select(sql)
        else:
            k = list(kwargs.keys())[0]
            v = kwargs.get(k)
            sql = "select * from %s where %s=?"%(cls.table_name,k)
            sql = sql.replace("?","%s")
            res = ms.select(sql,v)
        if res:
            return [cls(**r) for r in res]

    def my_update(self):
        ms = Mysql()
        fields = []
        values = []
        pk = None
        for k,v in self.mappings.items():
            if v.primary_key:
                pk = getattr(self,v.name)
            else:
                fields.append(k + "=?")
                values.append(getattr(self,k))
        sql = "update %s set %s where %s=%s"%(self.table_name,",".join(fields),self.primary_key,pk)
        sql = sql.replace("?","%s")
        ms.execute(sql,values)

    def save(self):
        ms = Mysql()
        fields = []
        values = []
        args = []
        for k,v in self.mappings.items():
            if v.primary_key:
                continue
            else:
                args.append("?")
                fields.append(k)
                values.append(getattr(self,k,v.default))
        sql = "insert into %s(%s) values(%s)"%(self.table_name,",".join(fields),",".join(args))
        sql = sql.replace("?","%s")
        ms.execute(sql,values)



