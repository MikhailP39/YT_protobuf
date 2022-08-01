# Converting the list of steps into a hierarchical structure
## Objective

The aim of the task is to verify problem solving skills using the python language.

## Description of the task

A file is given messages.proto:

```
syntax = 'proto3';

package messages;

message Request {
    message Step {
        int32 id = 1;
        optional int32 parent_id = 2;
        int32 duration = 3;
        string name = 4;
    }

    repeated Step steps = 1;
    optional int32 step_id = 2;
}

message Response {
    message HierarchicalStep {
        string name = 1;
        int32 duration = 2;
        repeated HierarchicalStep children = 3;
    }

    repeated HierarchicalStep hierarchical_step = 1;
    string max_duration_step_name = 2;
    int32 max_duration_step_duration = 3;
}
```
The input message described by the Request definition should be read and converted into the output Response message, in such a way that the list of steps "Step" is changed into a hierarchical step "HierarchicalStep".

In the "step_id" field there is an identifier of the step from which you should start building the structure.
If the value is not set, start with a step that does not have a value set in the "parent_id" field.
The list of "children" steps is to be sorted in descending order of the "duration" field.
In the "max_duration_step_name" field there is to be the name of the step which lasted the longest (the duration of a given step is the "duration" of a given step minus the sum of "duration" of its direct descendants), and in "max_duration_step_duration" the duration of this step.

## Result 

The result is a .py file with code meeting the requirements above. The code is to include a function that accepts a serialized Request message and returns a serialized Response message. There may also be other functions and classes that the main function will use.

Sample input: b'\n\x08\x08\x01\x18\x96\x01"\x01A\n\t\x08\x02\x10\x01\x18-"\x01B\n\t\x08\x03\x10\x01\x182"\x01C\n\t\x08\x04\x10\x02\x18\x14"\x01D\n\t\x08\x05\x10\x02\x18\x14"\x01E\x10\x01'

Sample output: b'\n"\n\x01A\x10\x96\x01\x1a\x05\n\x01C\x102\x1a\x13\n\x01B\x10-\x1a\x05\n\x01D\x10\x14\x1a\x05\n\x01E\x10\x14\x12\x01A\x187'
