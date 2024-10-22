from manim import *


class PIDGraphDemo(Scene):
    def construct(self):
        # set up graph
        axes = Axes(
            x_range=[0, 8, 1],  # Reduced from 13 to 8
            y_range=[-200, 50, 50],
            axis_config={"color": BLUE},
            x_axis_config={"numbers_to_include": []},
            y_axis_config={"numbers_to_include": range(-200, 50, 50)},
            x_length=round(config. frame_width) - 6,  # Reduce width to shrink x-axis
            y_length=round(config. frame_height) - 2
        )
        axes.shift(2 * RIGHT)

        x_label = Text('Error').scale(0.6).rotate(PI / 2).next_to(axes, LEFT)

        # data points for graph
        data = [-200, -100, -30, 5, 0, 0, 0, 0]
        points = [(p, i) for p, i in enumerate(data)]

        # curve of data points with smoothening
        curve = VMobject()
        curve.set_points_smoothly([axes.c2p(x, y) for x, y in points])
        curve.set_color(RED)

        # model car with target
        box = Square(side_length=0.5).set_fill(BLUE, opacity=1).set_stroke(width=0)
        target = Dot(color=GREEN).scale(1.5)
        target_label = Text("Target", font_size=24).next_to(target, RIGHT)

        box_x_pos = 6 * LEFT[0]  # X coordinate for box and target
        box.move_to([box_x_pos, axes.c2p(0, data[0])[1], 0])
        target.move_to([box_x_pos, axes.c2p(0, 0)[1], 0])
        target_label.next_to(target, RIGHT)

        # animation
        progress = ValueTracker(0)

        def update_box(b):
            t = progress.get_value()
            if t <= len(points) - 1:
                index = int(t)
                frac = t - index
                if index < len(points) - 1:
                    start = axes.c2p(points[index][0], points[index][1])
                    end = axes.c2p(points[index + 1][0], points[index + 1][1])
                    new_point = interpolate(start, end, frac)
                else:
                    new_point = axes.c2p(points[-1][0], points[-1][1])
                b.move_to([box_x_pos, new_point[1], 0])

        box.add_updater(update_box)

        self.play(
            Write(axes),
            Write(x_label),
            Create(target),
            Write(target_label),
            Create(box)
        )
        self.wait(1)
        self.play(
            Create(curve),
            progress.animate.set_value(len(points) - 1),
            run_time=2,
            rate_func=linear
        )
        self.wait(2)

        # remove updater
        box.clear_updaters()
