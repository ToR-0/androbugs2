class FilteringEngine:

    def __init__(self, enable_exclude_classes, str_regexp_type_excluded_classes):
        self.__enable_exclude_classes = enable_exclude_classes
        self.__str_regexp_type_excluded_classes = str_regexp_type_excluded_classes
        self.__regexp_excluded_classes = re.compile(self.__str_regexp_type_excluded_classes, re.I)

    def get_filtering_regexp(self):
        return self.__regexp_excluded_classes

    def filter_efficient_search_result_value(self, result):

        if result is None:
            return []
        if (not self.__enable_exclude_classes):
            return result

        l = []
        for found_string, method in result:
            if not self.__regexp_excluded_classes.match(method.get_class_name()):
                l.append((found_string, method))

        return l

    def is_class_name_not_in_exclusion(self, class_name):
        if self.__enable_exclude_classes:
            if self.__regexp_excluded_classes.match(class_name):
                return False
            else:
                return True
        else:
            return True

    def is_all_of_key_class_in_dict_not_in_exclusion(self, dict_result):
        if self.__enable_exclude_classes:
            isAllMatchExclusion = True
            for class_name, method_list in list(dict_result.items()):
                if not self.__regexp_excluded_classes.match(class_name):  # any match
                    isAllMatchExclusion = False

            if isAllMatchExclusion:
                return False

            return True
        else:
            return True

    def filter_list_of_methods(self, method_list):
        if self.__enable_exclude_classes and method_list:
            l = []
            for method in method_list:
                if not self.__regexp_excluded_classes.match(method.get_class_name()):
                    l.append(method)
            return l
        else:
            return method_list

    def filter_list_of_classes(self, class_list):
        if self.__enable_exclude_classes and class_list:
            l = []
            for i in class_list:
                if not self.__regexp_excluded_classes.match(i):
                    l.append(i)
            return l
        else:
            return class_list

    def filter_list_of_paths(self, vm, paths):
        if self.__enable_exclude_classes and paths:
            cm = vm.get_class_manager()

            l = []
            for path in paths:
                src_class_name, src_method_name, src_descriptor = path.get_src(cm)
                if not self.__regexp_excluded_classes.match(src_class_name):
                    l.append(path)

            return l
        else:
            return paths

    def filter_dst_class_in_paths(self, vm, paths, excluded_class_list):
        cm = vm.get_class_manager()

        l = []
        for path in paths:
            dst_class_name, _, _ = path.get_dst(cm)
            if dst_class_name not in excluded_class_list:
                l.append(path)

        return l

    def filter_list_of_variables(self, vm, paths):
        """
			Example paths input: [[('R', 8), 5050], [('R', 24), 5046]]
		"""

        if self.__enable_exclude_classes and paths:
            l = []
            for path in paths:
                access, idx = path[0]
                m_idx = path[1]
                method = vm.get_cm_method(m_idx)
                class_name = method[0]

                if not self.__regexp_excluded_classes.match(class_name):
                    l.append(path)
            return l
        else:
            return paths

    def get_class_container_dict_by_new_instance_classname_in_paths(self, vm, analysis, paths,
                                                                    result_idx):  # dic: key=>class_name, value=>paths
        dic_classname_to_paths = {}
        paths = self.filter_list_of_paths(vm, paths)
        for i in analysis.trace_Register_value_by_Param_in_source_Paths(vm, paths):
            if (i.getResult()[result_idx] is None) or (
                    not i.is_class_container(
                        result_idx)):  # If parameter 0 is a class_container type (ex: Lclass/name;)
                continue
            class_container = i.getResult()[result_idx]
            class_name = class_container.get_class_name()
            if class_name not in dic_classname_to_paths:
                dic_classname_to_paths[class_name] = []
            dic_classname_to_paths[class_name].append(i.getPath())
        return dic_classname_to_paths
