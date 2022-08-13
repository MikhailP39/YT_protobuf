"""Libraries."""
import messages_pb2 as Request
import messages_pb2 as Response
from google.protobuf.json_format import MessageToDict
from operator import itemgetter


def get_request(message_request):
    """Get Request message."""
    request = Request.Request()

    """Get Response message."""
    response = Response.Response()

    """Decode Request message."""
    request.ParseFromString(message_request)

    """Transform Request message to Dict."""
    dict_request = MessageToDict(request)

    """Create the Lists with steps"""
    list_steps = dict_request['steps']

    """Create the Parents, Children and Duration lists."""
    list_parents = []
    list_children = []
    list_duration = []

    """Fill the Parents, Children and Duration lists"""
    for i in range(len(list_steps)):
        dict_item = list_steps[i]
        list_duration.append(dict_item['duration'])
        if dict_item['id'] == dict_request['stepId'] or not dict_item['parentId']:
            list_parents.append(list_steps[i])
        else:
            list_children.append(list_steps[i])

    """Find the Max Duration."""
    max_duration = max(list_duration)

    """Sort Children List by the Duration"""
    list_children = sorted(list_children, key=itemgetter('duration'), reverse=True)

    """Sum of the Children Duration with ParentId"""
    sum_duration_children = []
    for p in range(len(list_parents)):
        for c in range(len(list_children)):
            children_item = list_children[c]
            parents_item = list_parents[p]
            if children_item['parentId'] == parents_item['id']:
                sum_duration_children.append(children_item['duration'])
    sum_duration_children = sum(sum_duration_children)

    # """Read the messages"""
    # print(list_duration)
    # print(list_parents)
    # print(list_children)
    # print(f"Max duration: {max_duration}")
    # print(f"Sorted Child List by Duration: {list_children}")
    # print(f"Sum duration of children: {sum_duration_children}")
    # print("------------------")

    """Set the Response Message"""
    parent_response = response.hierarchical_step.add()
    set_response(parent_response, list_parents, list_children, dict_request)

    """Fill Max Duration Step Name"""
    for i in range(len(list_steps)):
        dict_item = list_steps[i]
        if dict_item['duration'] == max_duration:
            response.max_duration_step_name = dict_item['name']

    """Fill Max Duration Step Duration"""
    response.max_duration_step_duration = max_duration - sum_duration_children

    """Transform Response message to the Bite."""
    message_response = response.SerializeToString()

    """Print the Byte response Message Result"""
    print(f"Output Message: {message_response}")


def set_response(parent_response, parents, children, dict_request):
    for p in range(len(parents)):
        for c in range(len(children)):
            children_item = children[c]
            parents_item = parents[p]
            if parents_item['id'] == dict_request['stepId'] or not parents_item['parentId']:
                parent_response.name = parents_item['name']
                parent_response.duration = parents_item['duration']
            if children_item['parentId'] == parents_item['id']:
                children_response = parent_response.children.add()
                children_response.name = children_item['name']
                children_response.duration = children_item['duration']
            else:
                children_response_else = children_response.children.add()
                children_response_else.name = children_item['name']
                children_response_else.duration = children_item['duration']


def main():
    input_mes = b'\n\x08\x08\x01\x18\x96\x01"\x01A\n\t\x08\x02\x10\x01\x18-"\x01B\n\t\x08\x03\x10\x01\x182"\x01C\n\t\x08\x04\x10\x02\x18\x14"\x01D\n\t\x08\x05\x10\x02\x18\x14"\x01E\x10\x01'
    #output_mes = b'\n"\n\x01A\x10\x96\x01\x1a\x05\n\x01C\x102\x1a\x13\n\x01B\x10-\x1a\x05\n\x01D\x10\x14\x1a\x05\n\x01E\x10\x14\x12\x01A\x187'
    get_request(input_mes)


if __name__ == "__main__":
    main()