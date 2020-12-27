import os, json, sys
import time, portalocker


class CustomError(Exception):
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return self.value


class Database:
    def __init__(self, name, location=os.getcwd()):
        self.absloc = os.path.join(location, name + ".json")
        self.key_value = {}
        try:
            if os.path.isfile(self.absloc) == False:
                self.file = open(self.absloc, "w")
                json.dump(self.key_value, self.file)
            else:
                self.file = open(self.absloc, "r")
                self.key_value = json.load(self.file)
            portalocker.lock(self.file, portalocker.LOCK_EX)
        except Exception as e:
            print(str(e) + " already Locked")
            sys.exit(0)
        self.file.flush()

    def read(self, key, lock=None):
        if lock is not None:
            lock.acquire()
        self.ttl()
        self.file = open(self.absloc, "r")
        self.key_value = json.load(self.file)
        try:
            if key in self.key_value:
                print(self.key_value[key]['value'])
            else:
                raise KeyError
        except KeyError:
            print("Read Fail: Key not Present")
        finally:
            if lock is not None:
                lock.release()

    def update(self):
        self.ttl()
        self.file = open(self.absloc, "r")
        self.key_value = json.load(self.file)

    def create(self, lock=None):
        if lock is not None:
            lock.acquire()
        self.update()
        if os.path.getsize(self.absloc) >= 1e+9:
            raise CustomError("Size of file has reached 1GB(max)")
        key = input("Enter Key:")
        try:
            if key in self.key_value:
                raise KeyError
            if len(key) > 32:
                raise CustomError("Size of Key should be less than or equal to 32 characters")
            value = json.dumps(input("Enter JSON value:"))
            if sys.getsizeof(value) > 1000:
                raise CustomError("Size of JSON object should be less than or equal to 16KB")
        except KeyError:
            print("Write Fail: Key already present")
        except CustomError as error:
            print(error.msg)
        else:
            ttl = int(input("Enter ttl in seconds:"))
            self.file = open(self.absloc, "w")
            self.key_value[key] = {"value": value, "ttl": ttl, "timestamp": time.time()}
            json.dump(self.key_value, self.file)
            self.file.flush()
        finally:
            if lock is not None:
                lock.release()

    def delete(self, key, lock=None):
        if lock is not None:
            lock.acquire()
        self.update()
        try:
            if key in self.key_value:
                del self.key_value[key]
                self.file = open(self.absloc, "w")
                json.dump(self.key_value, self.file)
                self.file.flush()
            else:
                raise KeyError
        except KeyError:
            print("Delete Fail: Key not present")
        finally:
            if lock is not None:
                lock.release()

    def ttl(self):
        current_time = time.time()
        keys = list(self.key_value)
        for key in keys:
            if self.key_value[key]["ttl"] <= current_time - self.key_value[key]["timestamp"]:
                del self.key_value[key]
        self.file = open(self.absloc, "w")
        json.dump(self.key_value, self.file)
        self.file.flush()

    def fileclose(self):
        self.file.close()
