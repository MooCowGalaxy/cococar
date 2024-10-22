from manim import *


class Dismiss(Animation):
    def __init__(self, mobject, direction=DOWN, fade_factor=2, rotation_angle=-PI/48, **kwargs):
        super().__init__(mobject, **kwargs)
        self.direction = direction
        self.fade_factor = fade_factor
        self.rotation_angle = rotation_angle

    def interpolate_mobject(self, alpha):
        alpha_faded = pow(1 - alpha, self.fade_factor)
        self.mobject.set_opacity(alpha_faded)
        self.mobject.shift(self.direction * alpha * 0.05)
        self.mobject.rotate(alpha * self.rotation_angle, about_point=self.mobject.get_center())


class LevelShifter(Scene):
    def construct(self):
        TEXT_SCALE = 0.6
        OBJECT_DISTANCE = 3

        self.wait(1)

        # create objects
        raspi = Square(color=BLUE, fill_opacity=0.3)
        raspi.set_fill(BLUE, 0.3)
        raspi.shift(OBJECT_DISTANCE * RIGHT)

        raspi_voltage = Text('3.3V')
        raspi_voltage.move_to([0, 0, 0])
        raspi_voltage.shift(OBJECT_DISTANCE * RIGHT)

        raspi_label = Text('Raspberry Pi').scale(TEXT_SCALE)
        raspi_label.move_to([0, 0, 0])
        raspi_label.shift(OBJECT_DISTANCE * RIGHT, 1.5 * DOWN)

        controller = Square(color=GREEN, fill_opacity=0.3)
        controller.set_fill(GREEN, 0.3)
        controller.shift(OBJECT_DISTANCE * LEFT)

        controller_voltage = Text('6V')
        controller_voltage.move_to([0, 0, 0])
        controller_voltage.shift(OBJECT_DISTANCE * LEFT)

        controller_label = Text('Motor Controller').scale(TEXT_SCALE)
        controller_label.move_to([0, 0.069 * TEXT_SCALE, 0])
        controller_label.shift(OBJECT_DISTANCE * LEFT, 1.5 * DOWN)

        self.play(
            Create(raspi),
            Create(controller),
            FadeIn(raspi_voltage),
            FadeIn(controller_voltage),
            Write(raspi_label, rate_func=smooth),
            Write(controller_label, rate_func=smooth),
            run_time=1
        )
        self.wait(1)

        # initial arrow pointing from RPi to controller with 3.3v label
        direct_arrow = Arrow(start=1.5 * RIGHT, end=1.5 * LEFT, color=WHITE)
        direct_arrow_label = Text('3.3V').scale(TEXT_SCALE)
        direct_arrow_label.move_to([0, 0.3, 0])

        self.play(
            Create(direct_arrow, run_time=0.5),
            FadeIn(direct_arrow_label, run_time=0.75)
        )
        self.wait(1)
        self.play(
            direct_arrow.animate.set_color(RED_B),
            direct_arrow_label.animate.set_color(RED_B),
            run_time=0.5
        )
        self.wait(1)
        self.play(
            Dismiss(direct_arrow, run_time=0.5),
            Dismiss(direct_arrow_label, run_time=0.5),
        )

        # shift all objects
        SHIFT_OBJECTS_LEFT = LEFT * 2
        SHIFT_OBJECTS_RIGHT = RIGHT * 2
        self.wait(0.25)
        self.play(
            raspi.animate.shift(SHIFT_OBJECTS_RIGHT),
            raspi_voltage.animate.shift(SHIFT_OBJECTS_RIGHT),
            raspi_label.animate.shift(SHIFT_OBJECTS_RIGHT),
            controller.animate.shift(SHIFT_OBJECTS_LEFT),
            controller_voltage.animate.shift(SHIFT_OBJECTS_LEFT),
            controller_label.animate.shift(SHIFT_OBJECTS_LEFT),
            run_time=0.5
        )

        # draw arrow to level shifter
        level_shifter = Square()
        level_shifter.set_fill(GRAY, 0.5)

        level_shifter_label = Text('Level Shifter').scale(TEXT_SCALE)
        level_shifter_label.move_to([0, 0.069 * TEXT_SCALE, 0])
        level_shifter_label.shift(1.5 * DOWN)

        raspi_arrow = Arrow(start=1.5 * RIGHT, end=1.5 * LEFT, color=WHITE)
        raspi_arrow_label = Text('3.3V').scale(TEXT_SCALE)
        raspi_arrow_label.move_to([0, 0.3, 0])
        raspi_arrow.shift(2.5 * RIGHT)
        raspi_arrow_label.shift(2.5 * RIGHT)

        controller_arrow = Arrow(start=1.5 * RIGHT, end=1.5 * LEFT, color=WHITE)
        controller_arrow_label = Text('6V').scale(TEXT_SCALE)
        controller_arrow_label.move_to([0, 0.3, 0])
        controller_arrow.shift(2.5 * LEFT)
        controller_arrow_label.shift(2.5 * LEFT)

        self.play(
            Create(level_shifter),
            Write(level_shifter_label, rate_func=smooth),
            run_time=1
        )
        self.play(
            Create(raspi_arrow, run_time=0.5),
            FadeIn(raspi_arrow_label, run_time=0.75),

            Create(controller_arrow, run_time=0.5),
            FadeIn(controller_arrow_label, run_time=0.75),
        )

        # make arrows green
        self.wait(0.5)
        self.play(
            raspi_arrow.animate.set_color(GREEN_C),
            raspi_arrow_label.animate.set_color(GREEN_C),
            controller_arrow.animate.set_color(GREEN_C),
            controller_arrow_label.animate.set_color(GREEN_C),
            run_time=0.5
        )
        self.wait(1)
