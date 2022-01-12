import json
from graphene import ObjectType, List, String, Schema, Field, Mutation


class CourseType(ObjectType):
    id = String(required=True)
    title = String(required=True)
    instructor = String(required=True)
    publish_date = String()


class Query(ObjectType):
    course_list = None
    get_course = List(CourseType)
    get_single_course = Field(List(CourseType), id=String())

    # Get
    async def resolve_get_course(self, info):
        with open("db/courses.json") as courses:
            course_list = json.load(courses)
        return course_list
    # Get One

    async def resolve_get_single_course(self, info, id=None):
        with open("db/courses.json") as courses:
            course_list = json.load(courses)
            if (id):
                for course in course_list:
                    if course['id'] == id:
                        return [course]
        return course_list


class CreateCourse(Mutation):
    course = Field(CourseType)

    class Arguments:
        id = String(required=True)
        title = String(required=True)
        instructor = String(required=True)

    async def mutate(self, info, id, title, instructor):
        with open("db/courses.json", "r+") as courses:
            course_list = json.load(courses)
            course_list.append(
                {"id": id, "title": title, "instructor": instructor})
            courses.seek(0)
            json.dump(course_list, courses, indent=2)
        return CreateCourse(course=course_list[-1])


class UpdateCourse(Mutation):
    course = Field(CourseType)

    class Arguments:
        id = String(required=True)
        title = String(required=True)
        instructor = String(required=True)

    async def mutate(self, info, id, title, instructor):
        course_list = None
        with open("db/courses.json", "r+") as courses:
            course_list = json.load(courses)
            for course in courses:
                if course['id'] == id:
                    course_list.remove(course)
            course_list.append(
                {"id": id, "title": title, "instructor": instructor})
            courses.seek(0)
            json.dump(course_list, courses, indent=2)

        return UpdateCourse(course=course_list[-1])


class DeleteCourse(Mutation):
    ok = String()

    class Arguments:
        id = String(required=True)

    async def mutate(self, info, id):
        course_list = None
        with open("db/courses.json", "r+") as courses:
            course_list = json.load(courses)
            for course in course_list:
                if course['id'] == id:
                    course_list.remove(course)

        with open("db/courses.json", "w+") as courses:
            json.dump(course_list, courses, indent=2)

        return DeleteCourse(ok=True)


class Mutation(ObjectType):
    create_course = CreateCourse.Field()
    update_course = UpdateCourse.Field()
    delete_course = DeleteCourse.Field()


courseSchema = Schema(query=Query, mutation=Mutation)
